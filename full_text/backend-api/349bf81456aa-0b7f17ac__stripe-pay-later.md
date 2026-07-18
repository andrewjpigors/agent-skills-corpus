---
name: stripe-pay-later
description: Enable Buy Now, Pay Later (BNPL) and flexible payment options using Stripe. Create payment intents, manage payment methods (Afterpay, Klarna, PayPal, Card), and handle pay later transactions. Use when customers need payment flexibility or to offer installment payment options.
license: Apache-2.0
metadata:
  author: agentskills
  version: "1.0"
  provider: Stripe
compatibility: Requires Stripe API key, Python 3.8+, stripe Python package
---

# Stripe Pay Later Skill

Enable flexible payment options including Buy Now, Pay Later (BNPL) and installment payments through Stripe.

## Overview

This skill provides agents with the ability to:
- **Create pay later payments** - Support Afterpay, Klarna, and other BNPL providers
- **Manage payment intents** - Handle payment processing and confirmation
- **Retrieve payment methods** - Query available payment options for customers
- **Confirm transactions** - Complete pay later purchases securely
- **Handle webhooks** - Listen for payment status updates

## What Stripe Pay Later Supports

Stripe's Pay Later product includes:
- **Afterpay** - Buy now, pay in 4 interest-free installments
- **Klarna** - Multiple payment options including pay later and installments
- **PayPal** - Flexible payment options through PayPal
- **Card payments** - Traditional credit/debit card processing

## Getting Started

### Prerequisites

1. Stripe account with Pay Later enabled
2. Stripe API keys (publishable and secret)
3. Python 3.8+
4. `stripe` Python package

### Configuration

Set up your environment variables:

```bash
export STRIPE_API_KEY="sk_live_your_key_here"
export STRIPE_PUBLISHABLE_KEY="pk_live_your_key_here"
```

### Basic Usage

#### Create a Pay Later Payment

```python
from scripts.pay_later import create_pay_later_payment

# Create a payment for a customer
payment = create_pay_later_payment(
    amount=10000,  # $100.00 in cents
    currency="usd",
    payment_method="afterpay_pay_now",
    customer_email="customer@example.com",
    description="Product purchase"
)

print(payment['client_secret'])
```

#### Confirm Payment

```python
from scripts.pay_later import confirm_payment

# Confirm the payment after customer authorization
confirmation = confirm_payment(
    payment_intent_id="pi_1234567890"
)
```

#### Get Available Payment Methods

```python
from scripts.pay_later import get_payment_methods

# List payment methods for a customer
methods = get_payment_methods(customer_id="cus_1234567890")
```

## API Reference

### Core Functions

#### `create_pay_later_payment()`

Create a new pay later payment intent.

**Parameters:**
- `amount` (int): Amount in cents
- `currency` (str): Currency code (e.g., "usd")
- `payment_method` (str): One of `afterpay_pay_now`, `klarna`, `paypal`, `card`
- `customer_email` (str): Customer email address
- `description` (str, optional): Payment description
- `metadata` (dict, optional): Custom metadata

**Returns:**
```python
{
    "id": "pi_1234567890",
    "client_secret": "pi_1234567890_secret_xxxxx",
    "status": "requires_action",
    "amount": 10000,
    "currency": "usd",
    "payment_method": "pm_1234567890"
}
```

#### `confirm_payment()`

Confirm and complete a payment intent.

**Parameters:**
- `payment_intent_id` (str): The payment intent ID
- `return_url` (str, optional): URL for redirect after confirmation

**Returns:**
```python
{
    "id": "pi_1234567890",
    "status": "succeeded",
    "charges": {...}
}
```

#### `get_payment_methods()`

List payment methods for a customer.

**Parameters:**
- `customer_id` (str): The Stripe customer ID
- `limit` (int, optional): Number of results to return (default: 10)

**Returns:**
```python
{
    "object": "list",
    "data": [
        {
            "id": "pm_1234567890",
            "type": "card",
            "billing_details": {...}
        }
    ]
}
```

## Security Considerations

- **Never expose secret API keys**: Use environment variables or secure vaults
- **Client-side confirmation**: For sensitive operations, use Stripe's client-side libraries
- **Webhook verification**: Always verify webhook signatures using `stripe.Webhook.construct_event()`
- **PCI compliance**: Card data is handled by Stripe; never store raw card details
- **Rate limiting**: Implement backoff strategies for API calls

## Best Practices

1. **Test mode first**: Use Stripe test keys (`sk_test_`) before going live
2. **Webhook monitoring**: Set up webhooks to track payment status changes
3. **Error handling**: Implement retry logic for failed transactions
4. **Customer notification**: Always inform customers about payment status
5. **Audit logging**: Log all payment transactions for compliance

## Examples

See the `scripts/` directory for complete working examples:
- `create_payment.py` - Create a new pay later payment
- `confirm_payment.py` - Confirm payment completion
- `list_payments.py` - Query payment history
- `webhook_handler.py` - Handle Stripe webhooks

## Resources

- [Stripe Pay Later Documentation](https://stripe.com/docs/payments/pay-later)
- [Stripe API Reference](https://stripe.com/docs/api)
- [Afterpay Integration Guide](https://stripe.com/docs/payments/afterpay)
- [Klarna Integration Guide](https://stripe.com/docs/payments/klarna)

## Support

For issues or questions:
1. Check Stripe's official documentation
2. Review error messages in Stripe dashboard
3. Test with Stripe test mode using test cards
4. Contact Stripe support for account-level issues
