document.addEventListener('DOMContentLoaded', async function() {
    flat_status = document.querySelector('#flat_status');
    flat_type = document.querySelector('#flat_type');
    price = document.querySelector('#price');
    add_cost = document.querySelector('#additional_cost');
    downpayment = document.querySelector('#downpayment');
    downpayment_type = document.querySelector('#downpayment_type');
    resale_levy = document.querySelector('#resale_levy');
    levy_res = document.querySelector('#levy_res');
    show_breakdown = document.querySelector('#show_breakdown');
    hide_breakdown = document.querySelector('#hide_breakdown');
    cost_breakdown = document.querySelector('#cost_breakdown');
    add_cost_res = document.querySelector('#additional_amt_res');
    downpayment_res = document.querySelector('#downpayment_res');
    conveyancing_fee = document.querySelector('#conveyancing_fee');
    stamp_fee = document.querySelector('#stamp_fee');
    lease_reg_fee = document.querySelector('#lease_reg_fee');
    mortage_reg_fee = document.querySelector('#mortage_reg_fee');
    stamp_duty = document.querySelector('#stamp_duty');
    survery_fee = document.querySelector('#survey_fee');
    loan_dropdown = document.querySelector('#loan_dropdown');
    loan_form = document.querySelector('#loan_form');
    loan_amount = document.querySelector('#loan_amount');
    loan_interest = document.querySelector('#loan_interest');
    loan_tenure = document.querySelector('#loan_tenure');
    loan_monthly = document.querySelector('#loan_monthly');
    total_repayment = document.querySelector('#total_repayment');
    reno_cost = document.querySelector('#reno_cost');
    reno_res = document.querySelector('#reno_res');
    agent_fee = document.querySelector('#agent_fee');
    agent_fee_res = document.querySelector('#agent_fee_res');
    total_cost = document.querySelector('#estimated_cost');

    function updateValues() {
        stamp_fee.value = (parseInt(price.value) + parseFloat(add_cost_res.value)) * 0.021;
        temp_price = parseInt(price.value);
        if (temp_price > 30000) {
            conveyancing_fee.value = 27;
            temp_price -= 30000;
        }
        else {
            conveyancing_fee.value = (temp_price / 1000) * 0.9;
            temp_price = 0;
        }
        if (temp_price > 30000) {
            conveyancing_fee.value = parseFloat(conveyancing_fee.value) + 21.6;
            temp_price -= 30000;
        }
        else {
            conveyancing_fee.value = parseFloat(conveyancing_fee.value) + (temp_price / 1000) * 0.72;
            temp_price = 0;
        }
        while (temp_price > 1000) {
            conveyancing_fee.value = parseFloat(conveyancing_fee.value) + 0.6;
            temp_price -= 1000;
        }
        conveyancing_fee.value = parseFloat(conveyancing_fee.value) + (temp_price / 1000) * 0.6;
        temp_price = 0;
        loan_monthly.value = ((parseInt(loan_amount.value) * parseFloat(loan_interest.value)) / (1200 * (1 - Math.pow(1 + (parseFloat(loan_interest.value) / 100), 1 - parseInt(loan_tenure.value))))).toFixed(2);
        if (!isNaN(parseFloat(loan_monthly.value) * parseInt(loan_tenure.value) * 12)) {
            total_repayment.value = (parseFloat(loan_monthly.value) * parseInt(loan_tenure.value) * 12).toFixed(2);
        }
        else {
            total_repayment.value = 0;
        }
        conveyancing_fee.value = (parseFloat(conveyancing_fee.value)).toFixed(2);
        stamp_fee.value = (parseFloat(stamp_fee.value)).toFixed(2);
        let values = [price.value, loan_amount.value, add_cost_res.value, agent_fee_res.value, downpayment_res.value, conveyancing_fee.value, stamp_fee.value, lease_reg_fee.value, mortage_reg_fee.value, reno_res.value, levy_res.value, stamp_duty.value, survery_fee.value, total_repayment.value]; // add all your values here
        total_cost.value = values.map(parseFloat).reduce((a, b) => a + b, 0);
    }

    flat_status.addEventListener('input', function() {
        if (flat_status.value == 'under_construction') {
            downpayment.style.display = 'block';
        }
        else {
            downpayment.style.display = 'none';
        }
    })
    downpayment_type.addEventListener('input', function() {
        if (downpayment_type.value == 'full') {
            downpayment_res.value = (parseInt(price.value) + parseFloat(add_cost_res.value)) / 10;
        }
        else if (downpayment_type.value == 'staggered') {
            downpayment_res.value = (parseInt(price.value) + parseFloat(add_cost_res.value)) / 20;
        }
        else if (downpayment_type.value == 'deferred') {
            downpayment_res.value = 0;
        }
        updateValues();
    })
    price.addEventListener('input', function() {
        if (parseInt(price.value) > 10000000) {
            price.value = 10000000;
        }
        updateValues();
    })
    flat_type.addEventListener('input', function() {
        if (flat_type.value == 2) {
            survey_fee.value = 163.50;
        }
        if (flat_type.value == 3) {
            survey_fee.value = 231.60;
        }
        if (flat_type.value == 4) {
            survey_fee.value = 299.75;
        }
        if (flat_type.value == 5) {
            survey_fee.value = 354.25;
        }
        if (flat_type.value == 'executive') {
            survey_fee.value = 408.75;
        }
        updateValues();
    })
    add_cost.addEventListener('input', function() {
        if (add_cost.value == 10000) {
            add_cost_res.value = 10000;
        }
        else if (add_cost.value == '5%') {
            add_cost_res.value = parseInt(price.value) * 0.05;
        }
        else if (add_cost.value == '10%') {
            add_cost_res.value = parseInt(price.value) * 0.1;
        }
        else if (add_cost.value == '20%') {
            add_cost_res.value = parseInt(price.value) * 0.2;
        }
        add_cost_res.value = parseFloat(add_cost_res.value).toFixed(2);
        updateValues();
    })
    loan_dropdown.addEventListener('input', function() {
        if (loan_dropdown.value == 'yes') {
            loan_form.style.display = 'block';
        }
        else {
            loan_form.style.display = 'none';
        }
    })
    loan_amount.addEventListener('input', function() {
        stamp_duty.value = parseInt(loan_amount.value) * 0.004;
    })
    loan_interest.addEventListener('input', function() {
        updateValues();
    })
    loan_tenure.addEventListener('input', function() {
        updateValues();
    })
    reno_cost.addEventListener('input', function() {
        reno_res.value = parseFloat(reno_cost.value);
    })
    resale_levy.addEventListener('input', function() {
        levy_res.value = parseFloat(resale_levy.value);
    })
    agent_fee.addEventListener('input', function() {
        agent_fee_res.value = (parseInt(price.value) / 100) * parseInt(agent_fee.value);
    })
    show_breakdown.addEventListener('click', function() {
        cost_breakdown.style.display = 'block';
        hide_breakdown.style.display = 'block';
        show_breakdown.style.display = 'none';
    })
    hide_breakdown.addEventListener('click', function() {
        cost_breakdown.style.display = 'none';
        show_breakdown.style.display = 'block';
        hide_breakdown.style.display = 'none';
    })
})
