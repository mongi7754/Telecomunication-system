# Fraud detection module: rule-based + ML stub
# The check_transaction(payload) function returns:
# { fraud_score: float, decision: 'APPROVE'|'REVIEW'|'BLOCK', reason: str }

def check_transaction(payload: dict):
    # Basic rule-based checks
    amount = float(payload.get('amount', 0))
    device_id = payload.get('device_id')
    ip = payload.get('ip_address')
    recent_failed = int(payload.get('recent_failed_attempts', 0))
    msisdn = payload.get('msisdn') or payload.get('phone') or ''
    score = 0.0
    reasons = []

    # Rule 1: Very high amount for first-time customer -> suspicious
    if amount > 100000:
        score += 0.6
        reasons.append('high_amount')

    # Rule 2: multiple failed attempts
    if recent_failed >= 3:
        score += 0.4
        reasons.append('failed_attempts')

    # Rule 3: blacklisted msisdn sample (for demo)
    blacklisted = ['+254700111111', '+254700222222']
    if msisdn in blacklisted:
        score = max(score, 0.9)
        reasons.append('blacklisted_number')

    # Rule 4: odd hours (e.g., 00:00 - 04:00)
    tod = payload.get('time_of_day')  # expected 0-23 integer
    try:
        tod = int(tod)
        if tod >=0 and tod <=4:
            score += 0.2
            reasons.append('odd_time')
    except:
        pass

    # Normalize score to 0-1
    if score > 1.0:
        score = 1.0

    # Placeholder: Hook for ML model
    # If you train a model and save it as 'model.joblib' in the app directory, you can import joblib and get a model prediction here.
    ml_score = 0.0
    try:
        import joblib, os
        model_path = os.path.join(os.path.dirname(__file__), 'model.joblib')
        if os.path.exists(model_path):
            model = joblib.load(model_path)
            # Create a feature vector (this is an example; adapt to your model)
            features = [
                float(amount),
                float(recent_failed),
            ]
            ml_pred = model.predict_proba([features])[0][1]  # probability of fraud
            ml_score = float(ml_pred)
    except Exception:
        # if model not present or joblib not installed, ignore
        ml_score = 0.0

    # Combine rule-based score and ml_score (simple average)
    final_score = (score + ml_score) / 2.0

    if final_score < 0.3:
        decision = 'APPROVE'
    elif final_score < 0.7:
        decision = 'REVIEW'
    else:
        decision = 'BLOCK'

    reason = ','.join(reasons) if reasons else 'no_rule_triggered'
    return {"fraud_score": round(final_score, 4), "decision": decision, "reason": reason}
