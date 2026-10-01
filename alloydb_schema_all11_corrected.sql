-- alloydb_schema_all11_corrected.sql
-- All 11 topics, TOPIC_<name> naming, matching pipeline_full11_corrected.py exactly.

-- T23 | account-loanslinesleases-lcm  -- The hub. accountLoanslinesleaseId (not the PK) is what every child actually links to.
CREATE TABLE TOPIC_account_loanslinesleases_lcm (
    account_loanslinesleases_lcm_id VARCHAR(40) PRIMARY KEY,
    account_loanslineslease_id VARCHAR(60) UNIQUE,
    application_number VARCHAR(60),
    application_system VARCHAR(60),
    bank_number VARCHAR(60),
    financial_instrument_number VARCHAR(60),
    obligation_number VARCHAR(60),
    obligor_number VARCHAR(60),
    external_source_tickler_reference VARCHAR(60)
);

-- T33 | product-rates  -- Standalone rate lookup, referenced by T11.
CREATE TABLE TOPIC_product_rates (
    product_rate_id VARCHAR(40) PRIMARY KEY,
    application_number VARCHAR(60),
    application_system VARCHAR(60),
    bank_number VARCHAR(60),
    effective_date VARCHAR(60),
    effective_time VARCHAR(60),
    external_source_customer_name_reference VARCHAR(60),
    rate_number VARCHAR(60),
    sequence_number VARCHAR(60)
);

-- T19 | customer-supplementals  -- Standalone in this diagram -- no drawn link to the loan side.
CREATE TABLE TOPIC_customer_supplementals (
    customer_supplemental_id VARCHAR(40) PRIMARY KEY,
    customer_id VARCHAR(60),
    application_number VARCHAR(60),
    application_system VARCHAR(60),
    bank_number VARCHAR(60),
    obligor_number VARCHAR(60)
);

-- T13 | account-loanslinesleases-lcm-postedtransactions  -- One loan, zero or many posted transactions.
CREATE TABLE TOPIC_account_loanslinesleases_lcm_postedtransactions (
    account_loanslinesleases_lcm_postedtransaction_id VARCHAR(40) PRIMARY KEY,
    account_loanslineslease_id VARCHAR(40) NOT NULL REFERENCES TOPIC_account_loanslinesleases_lcm(account_loanslineslease_id),
    application_number VARCHAR(60),
    application_system VARCHAR(60),
    bank_number VARCHAR(60),
    effective_date VARCHAR(60),
    financial_instrument_number VARCHAR(60),
    obligation_number VARCHAR(60),
    obligor_number VARCHAR(60),
    off_set_sequence_number VARCHAR(60),
    sequence_number VARCHAR(60),
    transaction_recorded_timestamp VARCHAR(60)
);

-- T26 | account-supplementals  -- Dashed in the diagram -- cardinality inferred, not explicitly confirmed.
CREATE TABLE TOPIC_account_supplementals (
    account_supplemental_id VARCHAR(40) PRIMARY KEY,
    account_id VARCHAR(40) NOT NULL REFERENCES TOPIC_account_loanslinesleases_lcm(account_loanslineslease_id),
    application_number VARCHAR(60),
    application_system VARCHAR(60),
    bank_number VARCHAR(60),
    financial_instrument_number VARCHAR(60),
    obligation_number VARCHAR(60),
    obligor_number VARCHAR(60)
);

-- T8 | account-loanslinesleases-chargeheaders  -- One loan, zero or many charge headers.
CREATE TABLE TOPIC_account_loanslinesleases_chargeheaders (
    account_loanslinesleases_chargeheader_id VARCHAR(40) PRIMARY KEY,
    account_loanslineslease_id VARCHAR(40) NOT NULL REFERENCES TOPIC_account_loanslinesleases_lcm(account_loanslineslease_id),
    application_number VARCHAR(60),
    application_system VARCHAR(60),
    bank_number VARCHAR(60),
    charge_code VARCHAR(60),
    financial_instrument_number VARCHAR(60),
    obligation_number VARCHAR(60),
    obligor_number VARCHAR(60)
);

-- T41 | account-relationships-accounts-supplemental  -- Dashed in the diagram -- cardinality inferred, not explicitly confirmed.
CREATE TABLE TOPIC_account_relationships_accounts_supplemental (
    account_relationships_accounts_supplemental_id VARCHAR(40) PRIMARY KEY,
    account_relationships_account_id VARCHAR(40) NOT NULL REFERENCES TOPIC_account_loanslinesleases_lcm(account_loanslineslease_id),
    application_system VARCHAR(60),
    financial_instrument_number VARCHAR(60),
    obligation_number VARCHAR(60)
);

-- T7 | account-loanslinesleases-balanceheaders  -- One loan, zero or many balance headers.
CREATE TABLE TOPIC_account_loanslinesleases_balanceheaders (
    account_loanslinesleases_balanceheader_id VARCHAR(40) PRIMARY KEY,
    account_loanslineslease_id VARCHAR(40) NOT NULL REFERENCES TOPIC_account_loanslinesleases_lcm(account_loanslineslease_id),
    application_system VARCHAR(60),
    associated_principal_balance_code VARCHAR(60),
    balance_code VARCHAR(60),
    bank_number VARCHAR(60),
    financial_instrument_number VARCHAR(60),
    obligation_number VARCHAR(60),
    obligor_number VARCHAR(60),
    sequence_number VARCHAR(60)
);

-- T11 | account-loanslinesleases-billingschedules  -- The only table with two parents -- needs both a loan AND a rate.
CREATE TABLE TOPIC_account_loanslinesleases_billingschedules (
    account_loanslinesleases_billingschedule_id VARCHAR(40) PRIMARY KEY,
    account_loanslineslease_id VARCHAR(40) NOT NULL REFERENCES TOPIC_account_loanslinesleases_lcm(account_loanslineslease_id),
    product_rate_id VARCHAR(40) NOT NULL REFERENCES TOPIC_product_rates(product_rate_id),
    application_number VARCHAR(60),
    application_system VARCHAR(60),
    bank_number VARCHAR(60),
    charge_code VARCHAR(60),
    effective_start_date VARCHAR(60),
    financial_instrument_number VARCHAR(60),
    obligation_number VARCHAR(60),
    obligor_number VARCHAR(60)
);

-- T12 | account-loanslinesleases-chargeheaders-amounts  -- Grandchild of T23 via T8.
CREATE TABLE TOPIC_account_loanslinesleases_chargeheaders_amounts (
    account_loanslinesleases_chargeheaders_amount_id VARCHAR(40) PRIMARY KEY,
    account_loanslinesleases_chargeheader_id VARCHAR(40) NOT NULL REFERENCES TOPIC_account_loanslinesleases_chargeheaders(account_loanslinesleases_chargeheader_id),
    amount_field_name VARCHAR(60),
    application_number VARCHAR(60),
    application_system VARCHAR(60),
    bank_number VARCHAR(60),
    charge_code VARCHAR(60),
    financial_instrument_number VARCHAR(60),
    obligation_number VARCHAR(60),
    obligor_number VARCHAR(60)
);

-- T15 | account-loanslinesleases-balanceheaders-amounts  -- Grandchild of T23 via T7.
CREATE TABLE TOPIC_account_loanslinesleases_balanceheaders_amounts (
    account_loanslinesleases_balanceheaders_amount_id VARCHAR(40) PRIMARY KEY,
    account_loanslinesleases_balanceheader_id VARCHAR(40) NOT NULL REFERENCES TOPIC_account_loanslinesleases_balanceheaders(account_loanslinesleases_balanceheader_id),
    amount_field_name VARCHAR(60),
    application_number VARCHAR(60),
    application_system VARCHAR(60),
    associated_principal_balance_code VARCHAR(60),
    balance_code VARCHAR(60),
    bank_number VARCHAR(60),
    financial_instrument_number VARCHAR(60),
    obligation_number VARCHAR(60),
    obligor_number VARCHAR(60),
    sequence_number VARCHAR(60)
);
