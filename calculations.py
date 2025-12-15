# © 2025 Raju Singh Rajpurohit. All rights reserved.
def calculate_investment(
    monthly_amount,
    years,
    annual_return,
    step_up_percent=0,
    expense_ratio=0,
    exit_load=0,
    tax_percentage=0,
    inflation_percentage=0,
    pause_months=0
):
    """
    WealthLens calculation engine
    Includes:
    - SIP / ETF
    - Step-up SIP
    - Expense ratio
    - Exit load
    - User-entered tax
    - Inflation-adjusted real value
    - SIP pause / missed months
    """

    # ---- Type safety ----
    monthly_amount = float(monthly_amount)
    years = int(years)

    annual_return = float(annual_return) / 100
    step_up_percent = float(step_up_percent) / 100
    expense_ratio = float(expense_ratio) / 100
    exit_load = float(exit_load) / 100
    tax_percentage = float(tax_percentage) / 100
    inflation_percentage = float(inflation_percentage) / 100
    pause_months = int(pause_months)

    # ---- Effective return (prevent crazy negatives) ----
    effective_return = max(annual_return - expense_ratio, -0.99)
    monthly_return = effective_return / 12

    total_months = years * 12

    total_invested = 0.0
    corpus = 0.0
    current_monthly = monthly_amount

    pause_counter = 0

    for month in range(1, total_months + 1):

        # Step-up at start of each year
        if month % 12 == 1 and month != 1:
            current_monthly *= (1 + step_up_percent)

        # SIP pause logic (limited to pause_months)
        if pause_counter < pause_months:
            pause_counter += 1
            corpus *= (1 + monthly_return)
            continue

        # Normal SIP month
        total_invested += current_monthly
        corpus = (corpus + current_monthly) * (1 + monthly_return)

    gross_final_value = corpus

    # Exit load
    exit_load_paid = gross_final_value * exit_load
    after_exit_load = gross_final_value - exit_load_paid

    # Tax on gains
    gains = after_exit_load - total_invested
    tax_paid = gains * tax_percentage if gains > 0 else 0.0
    final_after_tax = after_exit_load - tax_paid

    # Inflation-adjusted real value
    real_value = (
        final_after_tax / ((1 + inflation_percentage) ** years)
        if inflation_percentage > 0
        else final_after_tax
    )

    return {
        "total_invested": round(total_invested, 2),
        "gross_final_value": round(gross_final_value, 2),
        "expense_ratio_used": round(expense_ratio * 100, 2),
        "exit_load_paid": round(exit_load_paid, 2),
        "tax_percentage_used": round(tax_percentage * 100, 2),
        "tax_paid": round(tax_paid, 2),
        "final_value": round(final_after_tax, 2),
        "real_value_after_inflation": round(real_value, 2),
        "inflation_percentage_used": round(inflation_percentage * 100, 2),
        "pause_months": pause_months
    }
