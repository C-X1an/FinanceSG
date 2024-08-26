document.addEventListener("DOMContentLoaded", function (){
    loan = document.querySelector('#loan_checkbox');
    loan_form = document.querySelector('#loan_form');
    loan.addEventListener('click', function() {
        if (loan_form.style.display == 'block') {
            loan_form.style.display = 'none';
        }
        else {
            loan_form.style.display = 'block';
        }
    })
})

document.addEventListener("DOMContentLoaded", function (){
    scholarship = document.querySelector('#scholarship_checkbox');
    scholarship_form = document.querySelector('#scholarship_form');
    scholarship.addEventListener('click', function() {
        if (scholarship_form.style.display == 'block') {
            scholarship_form.style.display = 'none';
        }
        else {
            scholarship_form.style.display = 'block';
        }
    })
})

document.addEventListener('DOMContentLoaded', function() {
    let annual_cost = document.querySelector('#annual_cost');
    let academic_years = document.querySelector('#academic_years');
    let col = document.querySelector('#col');
    let annual_result = document.querySelector('#annual_result');
    let total_result = document.querySelector('#total_result');
    let loan_2 = document.querySelector('#loan_checkbox');
    let loan_amount = document.querySelector('#loan_amount');
    let loan_repayment = document.querySelector('#loan_repayment');
    let loan_interest = document.querySelector('#loan_interest');
    let scholarship_2 = document.querySelector('#scholarship_checkbox');
    let scholarship = document.querySelector('#scholarship_grant');


    function updateValues(){
        let temp_annual_result = parseInt(annual_cost.value) + parseInt(col.value);
        let temp_total_result = temp_annual_result * parseInt(academic_years.value);
        if (loan_2.checked == true) {
            var month = 0;
            var temp_loan_amount = parseInt(loan_amount.value);
            while (temp_loan_amount > parseInt(loan_repayment.value)) {
                month += 1;
                temp_loan_amount -= parseInt(loan_repayment.value);
                temp_total_result += parseInt(loan_repayment.value);
                if (month % 12 == 0) {
                    temp_loan_amount *= (parseInt(loan_interest.value) / 100);
                }
            }
            total_result.value = temp_total_result + temp_loan_amount;
        }
        if (scholarship_2.checked == true) {
            temp_annual_result = temp_annual_result - parseInt(scholarship.value);
            temp_total_result = temp_total_result - (parseInt(scholarship.value) * parseInt(academic_years.value));
        }
        total_result.value = '$' + (parseInt(temp_total_result));
        annual_result.value = '$' + (parseInt(temp_annual_result));
    }

    updateValues();

    annual_cost.addEventListener('input', function() {
        updateValues();
    })
    academic_years.addEventListener('input', function() {
        updateValues();
    })
    col.addEventListener('input', function() {
        updateValues();
    })
    loan_amount.addEventListener('input', function() {
        updateValues();
    })
    loan_repayment.addEventListener('input', function() {
        updateValues();
    })
    loan_interest.addEventListener('input', function() {
        updateValues();
    })
    scholarship.addEventListener('input', function() {
        updateValues();
    })

    loan_interest.addEventListener('input', function() {
        if (parseInt(loan_interest.value) > 10) {
            loan_interest.value = 10;
        }
    })
})
