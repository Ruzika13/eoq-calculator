import streamlit as st
import math
import matplotlib.pyplot as plt

def eoq_calculator(D, S, H):
    Q_star = math.sqrt((2 * D * S) / H)
    N = D / Q_star
    T = 365 / N
    ordering_cost = N * S
    holding_cost = (Q_star / 2) * H
    total_cost = ordering_cost + holding_cost

    return {
        "EOQ": round(Q_star, 2),
        "Orders_per_year": round(N, 2),
        "Days_between_orders": round(T, 1),
        "Annual_ordering_cost": round(ordering_cost, 2),
        "Annual_holding_cost": round(holding_cost, 2),
        "Total_annual_cost": round(total_cost, 2)
    }

st.set_page_config(page_title="EOQ Calculator", layout="centered")
st.title("📦 EOQ Calculator")
st.markdown("Find the optimal order quantity that minimizes total inventory costs.")

col1, col2, col3 = st.columns(3)
with col1:
    demand = st.number_input("Annual demand (D)", min_value=1, value=10000, step=100)
with col2:
    order_cost = st.number_input("Ordering cost per order (S)", min_value=0.0, value=50.0, step=1.0)
with col3:
    holding_cost = st.number_input("Holding cost per unit/year (H)", min_value=0.01, value=2.0, step=0.1)

results = eoq_calculator(demand, order_cost, holding_cost)

st.subheader("📊 Results")
cols = st.columns(3)
cols[0].metric("Optimal Order Quantity (Q*)", results["EOQ"])
cols[1].metric("Orders per Year", results["Orders_per_year"])
cols[2].metric("Days Between Orders", results["Days_between_orders"])

st.write("---")
col_cost1, col_cost2, col_cost3 = st.columns(3)
col_cost1.metric("Annual Ordering Cost", f"${results['Annual_ordering_cost']:,.2f}")
col_cost2.metric("Annual Holding Cost", f"${results['Annual_holding_cost']:,.2f}")
col_cost3.metric("Total Annual Cost", f"${results['Total_annual_cost']:,.2f}")

st.subheader("📈 Cost vs. Order Quantity")
Q_range = range(max(1, int(results["EOQ"]*0.3)), int(results["EOQ"]*2.5), 10)
order_costs = [(demand / Q) * order_cost for Q in Q_range]
hold_costs = [(Q / 2) * holding_cost for Q in Q_range]
total_costs = [oc + hc for oc, hc in zip(order_costs, hold_costs)]

fig, ax = plt.subplots()
ax.plot(Q_range, order_costs, label="Ordering Cost", linestyle="--")
ax.plot(Q_range, hold_costs, label="Holding Cost", linestyle="--")
ax.plot(Q_range, total_costs, label="Total Cost", linewidth=2)
ax.axvline(results["EOQ"], color="red", linestyle=":", label=f"EOQ = {results['EOQ']}")
ax.set_xlabel("Order Quantity")
ax.set_ylabel("Annual Cost ($)")
ax.legend()
ax.grid(True)
st.pyplot(fig)

st.caption("Cost curves show the trade‑off: too few orders → high ordering cost; too many → high holding cost. The EOQ balances them.")
