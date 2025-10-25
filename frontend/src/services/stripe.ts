import { loadStripe } from '@stripe/stripe-js';
import type { Stripe, StripeCardElement } from '@stripe/stripe-js';

// Initialize Stripe with publishable key
let stripePromise: Promise<Stripe | null> | null = null;

export const getStripe = (publishableKey?: string) => {
  if (!stripePromise && publishableKey) {
    stripePromise = loadStripe(publishableKey);
  }
  return stripePromise;
};

export const createPaymentMethod = async (
  stripe: Stripe,
  cardElement: StripeCardElement,
  billingDetails: {
    name: string;
    email: string;
  }
) => {
  const { error, paymentMethod } = await stripe.createPaymentMethod({
    type: 'card',
    card: cardElement,
    billing_details: billingDetails,
  });

  if (error) {
    throw new Error(error.message || 'Failed to create payment method');
  }

  return paymentMethod;
};

export const confirmCardPayment = async (
  stripe: Stripe,
  clientSecret: string,
  cardElement: StripeCardElement,
  billingDetails: {
    name: string;
    email: string;
  }
) => {
  const { error, paymentIntent } = await stripe.confirmCardPayment(clientSecret, {
    payment_method: {
      card: cardElement,
      billing_details: billingDetails,
    },
  });

  if (error) {
    throw new Error(error.message || 'Payment failed');
  }

  return paymentIntent;
};

export const createSubscription = async (
  stripe: Stripe,
  priceId: string,
  cardElement: StripeCardElement,
  billingDetails: {
    name: string;
    email: string;
  }
) => {
  // Create payment method
  const paymentMethod = await createPaymentMethod(stripe, cardElement, billingDetails);

  // Create subscription on backend
  const response = await fetch('/api/payments/subscription/create/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include',
    body: JSON.stringify({
      plan_id: priceId,
      payment_method_id: paymentMethod.id,
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error || 'Failed to create subscription');
  }

  const data = await response.json();

  // Confirm payment if client secret is provided
  if (data.client_secret) {
    const paymentIntent = await confirmCardPayment(
      stripe,
      data.client_secret,
      cardElement,
      billingDetails
    );

    return {
      subscription: data.subscription,
      paymentIntent,
    };
  }

  return data;
};