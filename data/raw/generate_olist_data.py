"""
Generate realistic Olist-like CSV data for the e-commerce analysis project.
Based on the real Olist Brazilian E-Commerce dataset structure.
"""
import pandas as pd
import numpy as np
import os
import random
from datetime import datetime, timedelta

random.seed(42)
np.random.seed(42)

OUT = os.path.dirname(os.path.abspath(__file__))

# ── helpers ─────────────────────────────────────────────────────────────────
def rand_id(n=32):
    return ''.join(random.choices('abcdef0123456789', k=n))

def rand_date(start='2016-10-01', end='2018-08-31'):
    s = pd.Timestamp(start)
    e = pd.Timestamp(end)
    delta = (e - s).days
    return s + pd.Timedelta(days=random.randint(0, delta),
                            hours=random.randint(0, 23),
                            minutes=random.randint(0, 59))

STATES = ['SP','RJ','MG','RS','PR','SC','BA','GO','PE','CE',
          'AM','ES','MT','MS','RN','PB','MA','PI','AL','SE']
STATE_WEIGHT = [30,15,12,8,7,6,5,3,3,3,2,2,1,1,1,1,1,1,1,1]

CATEGORIES = {
    'cama_mesa_banho': 12, 'beleza_saude': 11, 'esporte_lazer': 10,
    'informatica_acessorios': 9, 'moveis_decoracao': 8, 'utilidades_domesticas': 7,
    'relogios_presentes': 7, 'automotivo': 6, 'brinquedos': 5,
    'ferramentas_jardim': 4, 'telefonia': 4, 'eletronicos': 4,
    'malas_acessorios': 3, 'livros_tecnicos': 2, 'pet_shop': 2,
    'papelaria': 1, 'alimentos': 1
}
CATEGORY_NAMES = list(CATEGORIES.keys())
CATEGORY_WEIGHTS = list(CATEGORIES.values())

PAYMENT_TYPES = ['credit_card','boleto','voucher','debit_card']
PAYMENT_WEIGHTS = [74, 19, 5, 2]

ORDER_STATUSES = ['delivered','shipped','canceled','unavailable','invoiced','processing','approved','created']
ORDER_STATUS_W = [97, 1, 1, 0.3, 0.3, 0.2, 0.1, 0.1]

# ── 1. customers ────────────────────────────────────────────────────────────
N_CUSTOMERS = 99441
print(f"Generating {N_CUSTOMERS} customers...")
customer_ids = [rand_id() for _ in range(N_CUSTOMERS)]
customer_unique_ids = [rand_id() for _ in range(N_CUSTOMERS)]
customer_states = random.choices(STATES, weights=STATE_WEIGHT, k=N_CUSTOMERS)
customers_df = pd.DataFrame({
    'customer_id': customer_ids,
    'customer_unique_id': customer_unique_ids,
    'customer_zip_code_prefix': np.random.randint(10000, 99999, N_CUSTOMERS),
    'customer_city': ['sao paulo' if s=='SP' else 'rio de janeiro' if s=='RJ'
                      else 'belo horizonte' if s=='MG' else 'porto alegre' if s=='RS'
                      else 'curitiba' for s in customer_states],
    'customer_state': customer_states
})
customers_df.to_csv(os.path.join(OUT, 'olist_customers_dataset.csv'), index=False)
print("  -> customers done")

# ── 2. orders ───────────────────────────────────────────────────────────────
N_ORDERS = 99441
print(f"Generating {N_ORDERS} orders...")
order_ids = [rand_id() for _ in range(N_ORDERS)]
purchase_dates = [rand_date() for _ in range(N_ORDERS)]
purchase_dates_sorted = sorted(purchase_dates)

statuses = random.choices(ORDER_STATUSES, weights=ORDER_STATUS_W, k=N_ORDERS)
approved_offsets = [timedelta(hours=random.uniform(0.1, 2)) for _ in range(N_ORDERS)]
delivered_carrier_offsets = [timedelta(days=random.uniform(1, 5)) for _ in range(N_ORDERS)]
delivered_customer_offsets = [timedelta(days=random.uniform(5, 25)) for _ in range(N_ORDERS)]
estimated_offsets = [timedelta(days=random.uniform(20, 40)) for _ in range(N_ORDERS)]

orders_df = pd.DataFrame({
    'order_id': order_ids,
    'customer_id': random.choices(customer_ids, k=N_ORDERS),
    'order_status': statuses,
    'order_purchase_timestamp': [d.strftime('%Y-%m-%d %H:%M:%S') for d in purchase_dates],
    'order_approved_at': [(d + ao).strftime('%Y-%m-%d %H:%M:%S') for d, ao in zip(purchase_dates, approved_offsets)],
    'order_delivered_carrier_date': [(d + dc).strftime('%Y-%m-%d %H:%M:%S') for d, dc in zip(purchase_dates, delivered_carrier_offsets)],
    'order_delivered_customer_date': [(d + dcu).strftime('%Y-%m-%d %H:%M:%S') if st == 'delivered' else None
                                       for d, dcu, st in zip(purchase_dates, delivered_customer_offsets, statuses)],
    'order_estimated_delivery_date': [(d + eo).strftime('%Y-%m-%d %H:%M:%S') for d, eo in zip(purchase_dates, estimated_offsets)]
})
orders_df.to_csv(os.path.join(OUT, 'olist_orders_dataset.csv'), index=False)
print("  -> orders done")

# ── 3. order_items ──────────────────────────────────────────────────────────
print("Generating order items...")
N_SELLERS = 3095
seller_ids = [rand_id() for _ in range(N_SELLERS)]
N_PRODUCTS = 32951
product_ids = [rand_id() for _ in range(N_PRODUCTS)]

items_records = []
for oid in order_ids:
    n_items = random.choices([1, 2, 3, 4, 5], weights=[70, 18, 7, 3, 2])[0]
    for seq in range(1, n_items + 1):
        price = round(np.random.lognormal(4.0, 0.8), 2)
        price = max(5.0, min(price, 6735.0))
        items_records.append({
            'order_id': oid,
            'order_item_id': seq,
            'product_id': random.choice(product_ids),
            'seller_id': random.choice(seller_ids),
            'shipping_limit_date': (rand_date()).strftime('%Y-%m-%d %H:%M:%S'),
            'price': price,
            'freight_value': round(random.uniform(5, 80), 2)
        })

order_items_df = pd.DataFrame(items_records)
order_items_df.to_csv(os.path.join(OUT, 'olist_order_items_dataset.csv'), index=False)
print(f"  -> order_items done ({len(order_items_df)} rows)")

# ── 4. products ──────────────────────────────────────────────────────────────
print("Generating products...")
products_df = pd.DataFrame({
    'product_id': product_ids,
    'product_category_name': random.choices(CATEGORY_NAMES, weights=CATEGORY_WEIGHTS, k=N_PRODUCTS),
    'product_name_lenght': np.random.randint(10, 60, N_PRODUCTS),
    'product_description_lenght': np.random.randint(50, 2000, N_PRODUCTS),
    'product_photos_qty': np.random.randint(1, 10, N_PRODUCTS),
    'product_weight_g': np.random.randint(100, 30000, N_PRODUCTS),
    'product_length_cm': np.random.randint(10, 100, N_PRODUCTS),
    'product_height_cm': np.random.randint(5, 60, N_PRODUCTS),
    'product_width_cm': np.random.randint(10, 100, N_PRODUCTS)
})
products_df.to_csv(os.path.join(OUT, 'olist_products_dataset.csv'), index=False)
print("  -> products done")

# ── 5. sellers ───────────────────────────────────────────────────────────────
print("Generating sellers...")
sellers_df = pd.DataFrame({
    'seller_id': seller_ids,
    'seller_zip_code_prefix': np.random.randint(10000, 99999, N_SELLERS),
    'seller_city': random.choices(['sao paulo','rio de janeiro','belo horizonte','curitiba','porto alegre'], k=N_SELLERS),
    'seller_state': random.choices(STATES, weights=STATE_WEIGHT, k=N_SELLERS)
})
sellers_df.to_csv(os.path.join(OUT, 'olist_sellers_dataset.csv'), index=False)
print("  -> sellers done")

# ── 6. order_payments ────────────────────────────────────────────────────────
print("Generating payments...")
payment_records = []
for oid in order_ids:
    n_pay = random.choices([1, 2], weights=[90, 10])[0]
    for seq in range(1, n_pay + 1):
        payment_records.append({
            'order_id': oid,
            'payment_sequential': seq,
            'payment_type': random.choices(PAYMENT_TYPES, weights=PAYMENT_WEIGHTS)[0],
            'payment_installments': random.choices(range(1, 13), weights=[30,15,12,10,8,6,5,4,3,3,2,2])[0],
            'payment_value': round(np.random.lognormal(4.2, 0.75), 2)
        })
payments_df = pd.DataFrame(payment_records)
payments_df.to_csv(os.path.join(OUT, 'olist_order_payments_dataset.csv'), index=False)
print(f"  -> payments done ({len(payments_df)} rows)")

# ── 7. order_reviews ─────────────────────────────────────────────────────────
print("Generating reviews...")
SAMPLE_REVIEWS = random.sample(order_ids, int(N_ORDERS * 0.85))
reviews_df = pd.DataFrame({
    'review_id': [rand_id() for _ in SAMPLE_REVIEWS],
    'order_id': SAMPLE_REVIEWS,
    'review_score': random.choices([1,2,3,4,5], weights=[5,3,8,20,64], k=len(SAMPLE_REVIEWS)),
    'review_comment_title': [random.choice(['Ótimo!','Bom','Péssimo','Recomendo','Ok','Excelente',None,None,None]) for _ in SAMPLE_REVIEWS],
    'review_comment_message': [random.choice(['Produto chegou no prazo.','Muito bom!','Não gostei.',None,None,None,'Superou expectativas.']) for _ in SAMPLE_REVIEWS],
    'review_creation_date': [rand_date('2016-10-01','2018-09-15').strftime('%Y-%m-%d %H:%M:%S') for _ in SAMPLE_REVIEWS],
    'review_answer_timestamp': [rand_date('2016-10-01','2018-09-30').strftime('%Y-%m-%d %H:%M:%S') for _ in SAMPLE_REVIEWS]
})
reviews_df.to_csv(os.path.join(OUT, 'olist_order_reviews_dataset.csv'), index=False)
print("  -> reviews done")

# ── 8. category translation ──────────────────────────────────────────────────
cat_translation = {
    'cama_mesa_banho': 'bed_bath_table', 'beleza_saude': 'health_beauty',
    'esporte_lazer': 'sports_leisure', 'informatica_acessorios': 'computers_accessories',
    'moveis_decoracao': 'furniture_decor', 'utilidades_domesticas': 'housewares',
    'relogios_presentes': 'watches_gifts', 'automotivo': 'auto',
    'brinquedos': 'toys', 'ferramentas_jardim': 'garden_tools',
    'telefonia': 'telephony', 'eletronicos': 'electronics',
    'malas_acessorios': 'luggage_accessories', 'livros_tecnicos': 'books_technical',
    'pet_shop': 'pet_shop', 'papelaria': 'stationery', 'alimentos': 'food'
}
cat_df = pd.DataFrame({
    'product_category_name': list(cat_translation.keys()),
    'product_category_name_english': list(cat_translation.values())
})
cat_df.to_csv(os.path.join(OUT, 'product_category_name_translation.csv'), index=False)
print("  -> category translation done")

print("\n✅ All Olist CSV files generated successfully!")
print(f"   Location: {OUT}")
