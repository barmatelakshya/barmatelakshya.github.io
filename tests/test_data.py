"""
Test Data for SIH PS1 Cybersecurity Threat Detector
"""

# Phishing text samples
PHISHING_SAMPLES = [
    {
        'text': 'URGENT SECURITY ALERT! Your account will be suspended in 24 hours due to suspicious activity. Click here immediately to verify your identity.',
        'expected_phishing': True,
        'expected_confidence': 0.8
    },
    {
        'text': 'Congratulations! You have won $1,000,000 in our international lottery! Click here to claim your prize now before it expires!',
        'expected_phishing': True,
        'expected_confidence': 0.9
    },
    {
        'text': 'Your PayPal account has been limited due to unusual activity. Please verify your account immediately to avoid permanent suspension.',
        'expected_phishing': True,
        'expected_confidence': 0.8
    },
    {
        'text': 'FINAL NOTICE: Your subscription expires today! Act now to avoid service interruption. Update your payment method here.',
        'expected_phishing': True,
        'expected_confidence': 0.7
    }
]

# Legitimate text samples
LEGITIMATE_SAMPLES = [
    {
        'text': 'Thank you for your recent purchase from Amazon. Your order has been shipped and will arrive within 2-3 business days.',
        'expected_phishing': False,
        'expected_confidence': 0.1
    },
    {
        'text': 'Your monthly bank statement is now available. You can view it by logging into your online banking account.',
        'expected_phishing': False,
        'expected_confidence': 0.1
    },
    {
        'text': 'Reminder: Your appointment with Dr. Smith is scheduled for tomorrow at 2:00 PM. Please arrive 15 minutes early.',
        'expected_phishing': False,
        'expected_confidence': 0.05
    },
    {
        'text': 'Welcome to our newsletter! Here are this week\'s top technology news and updates from our editorial team.',
        'expected_phishing': False,
        'expected_confidence': 0.05
    }
]

# Suspicious URLs
SUSPICIOUS_URLS = [
    {
        'url': 'http://192.168.1.100/login.php',
        'expected_risk': 'High',
        'expected_score': 0.7
    },
    {
        'url': 'http://bit.ly/suspicious-link',
        'expected_risk': 'Medium',
        'expected_score': 0.5
    },
    {
        'url': 'http://secure-bank-verify.fake-domain.com/urgent-login',
        'expected_risk': 'High',
        'expected_score': 0.8
    },
    {
        'url': 'http://paypal-security-update.suspicious.com/verify?token=aGVsbG93b3JsZA==',
        'expected_risk': 'High',
        'expected_score': 0.8
    }
]

# Safe URLs
SAFE_URLS = [
    {
        'url': 'https://amazon.com/orders',
        'expected_risk': 'Low',
        'expected_score': 0.1
    },
    {
        'url': 'https://github.com/microsoft/vscode',
        'expected_risk': 'Low',
        'expected_score': 0.1
    },
    {
        'url': 'https://stackoverflow.com/questions/tagged/python',
        'expected_risk': 'Low',
        'expected_score': 0.1
    }
]

# Combined test cases
COMBINED_TEST_CASES = [
    {
        'name': 'High Risk: Phishing Text + Suspicious URL',
        'text': 'URGENT! Your account will be suspended. Click here to verify: http://secure-bank-verify.fake-domain.com/urgent-login',
        'url': 'http://secure-bank-verify.fake-domain.com/urgent-login',
        'expected_risk': 'Critical',
        'expected_score': 0.8
    },
    {
        'name': 'Medium Risk: Phishing Text Only',
        'text': 'Congratulations! You have won $1000! Click to claim now!',
        'url': '',
        'expected_risk': 'Medium',
        'expected_score': 0.6
    },
    {
        'name': 'Medium Risk: Suspicious URL Only',
        'text': '',
        'url': 'http://192.168.1.100/login.php?redirect=bank-verify',
        'expected_risk': 'Medium',
        'expected_score': 0.5
    },
    {
        'name': 'Low Risk: Safe Text + Safe URL',
        'text': 'Thank you for your Amazon purchase. Your order will arrive soon.',
        'url': 'https://amazon.com/orders',
        'expected_risk': 'Low',
        'expected_score': 0.1
    }
]

# Performance test data
PERFORMANCE_TEST_DATA = [
    ('URGENT! Verify now!', 'http://suspicious.com'),
    ('Thank you for purchase', 'https://amazon.com'),
    ('Click here now!', 'http://bit.ly/test'),
    ('Your order shipped', 'https://fedex.com'),
    ('Account suspended!', 'http://192.168.1.1')
] * 10  # Multiply for batch testing
