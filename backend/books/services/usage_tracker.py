# books/services/usage_tracker.py
import json
import time
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
import threading

class UsageTracker:
    """
    Enhanced token usage tracker with analytics and optimization features
    """

    def __init__(self):
        self.usage_file = Path("token_usage.json")
        # OpenRouter DeepSeek R1T2 Chimera pricing (as of 2024)
        self.pricing = {
            'input_tokens': 0.55 / 1000000,  # $0.55 per 1M input tokens
            'output_tokens': 2.19 / 1000000,  # $2.19 per 1M output tokens
        }
        self.monthly_limit = 87700000000  # 87.7B tokens (adjust based on actual limits)
        self._lock = threading.Lock()  # Thread safety for concurrent access

    def record_usage(self, input_tokens, output_tokens, model="deepseek/deepseek-r1-turbo", operation="generation"):
        """
        Record detailed token usage with cost calculation

        Args:
            input_tokens: Number of input tokens used
            output_tokens: Number of output tokens used
            model: AI model used
            operation: Type of operation (generation, cover_design, etc.)
        """
        with self._lock:
            try:
                data = self._load_usage_data()

                # Calculate costs
                input_cost = input_tokens * self.pricing['input_tokens']
                output_cost = output_tokens * self.pricing['output_tokens']
                total_cost = input_cost + output_cost
                total_tokens = input_tokens + output_tokens

                # Update current month totals
                current_month = datetime.now().strftime('%Y-%m')
                if current_month not in data['monthly_usage']:
                    data['monthly_usage'][current_month] = {
                        'total_tokens': 0,
                        'total_cost': 0.0,
                        'input_tokens': 0,
                        'output_tokens': 0,
                        'operations': defaultdict(int),
                        'models': defaultdict(int)
                    }

                month_data = data['monthly_usage'][current_month]
                month_data['total_tokens'] += total_tokens
                month_data['total_cost'] += total_cost
                month_data['input_tokens'] += input_tokens
                month_data['output_tokens'] += output_tokens
                month_data['operations'][operation] += 1
                month_data['models'][model] += total_tokens

                # Update overall totals
                data['total_tokens'] += total_tokens
                data['total_cost'] += total_cost
                data['total_input_tokens'] += input_tokens
                data['total_output_tokens'] += output_tokens

                # Record individual operation
                operation_record = {
                    'timestamp': datetime.now().isoformat(),
                    'model': model,
                    'operation': operation,
                    'input_tokens': input_tokens,
                    'output_tokens': output_tokens,
                    'total_tokens': total_tokens,
                    'cost': total_cost
                }
                data['operations'].append(operation_record)

                # Keep only last 1000 operations to prevent file bloat
                if len(data['operations']) > 1000:
                    data['operations'] = data['operations'][-1000:]

                self._save_usage_data(data)

                # Check limits and warn if approaching
                self._check_limits(month_data)

                return {
                    'tokens_used': total_tokens,
                    'cost': total_cost,
                    'remaining_monthly': self.get_remaining_tokens()
                }

            except Exception as e:
                print(f"Usage tracking error: {e}")
                return None

    def get_remaining_tokens(self):
        """Get remaining tokens for the current month"""
        try:
            data = self._load_usage_data()
            current_month = datetime.now().strftime('%Y-%m')
            used = data['monthly_usage'].get(current_month, {}).get('total_tokens', 0)
            return max(0, self.monthly_limit - used)
        except:
            return self.monthly_limit

    def get_usage_stats(self, months_back=1):
        """
        Get comprehensive usage statistics

        Args:
            months_back: Number of months to include in stats

        Returns:
            dict: Usage statistics
        """
        try:
            data = self._load_usage_data()
            current_month = datetime.now()
            stats = {}

            for i in range(months_back):
                month_key = (current_month - timedelta(days=i*30)).strftime('%Y-%m')
                if month_key in data['monthly_usage']:
                    stats[month_key] = data['monthly_usage'][month_key]

            return {
                'monthly_stats': stats,
                'overall_totals': {
                    'total_tokens': data['total_tokens'],
                    'total_cost': data['total_cost'],
                    'total_input_tokens': data['total_input_tokens'],
                    'total_output_tokens': data['total_output_tokens'],
                    'remaining_monthly': self.get_remaining_tokens()
                },
                'efficiency_metrics': self._calculate_efficiency_metrics(data)
            }
        except Exception as e:
            print(f"Error getting usage stats: {e}")
            return {}

    def _calculate_efficiency_metrics(self, data):
        """Calculate efficiency metrics for optimization"""
        try:
            if data['total_tokens'] == 0:
                return {}

            # Calculate average tokens per operation
            total_operations = len(data['operations'])
            if total_operations == 0:
                return {}

            avg_input_tokens = data['total_input_tokens'] / total_operations
            avg_output_tokens = data['total_output_tokens'] / total_operations
            avg_total_tokens = data['total_tokens'] / total_operations
            avg_cost_per_operation = data['total_cost'] / total_operations

            # Calculate cost efficiency (lower is better)
            cost_per_token = data['total_cost'] / data['total_tokens'] if data['total_tokens'] > 0 else 0

            return {
                'avg_input_tokens_per_operation': round(avg_input_tokens, 2),
                'avg_output_tokens_per_operation': round(avg_output_tokens, 2),
                'avg_total_tokens_per_operation': round(avg_total_tokens, 2),
                'avg_cost_per_operation': round(avg_cost_per_operation, 4),
                'cost_per_token': round(cost_per_token, 8),
                'total_operations': total_operations
            }
        except Exception as e:
            print(f"Error calculating efficiency metrics: {e}")
            return {}

    def _check_limits(self, month_data):
        """Check usage limits and provide warnings"""
        used_percentage = (month_data['total_tokens'] / self.monthly_limit) * 100

        if used_percentage > 95:
            print(f"CRITICAL: Used {used_percentage:.1f}% of monthly token limit!")
        elif used_percentage > 80:
            print(f"WARNING: Used {used_percentage:.1f}% of monthly token limit")
        elif used_percentage > 50:
            print(f"INFO: Used {used_percentage:.1f}% of monthly token limit")

    def _load_usage_data(self):
        """Load usage data from file with error handling"""
        try:
            if self.usage_file.exists():
                with open(self.usage_file, 'r') as f:
                    data = json.load(f)
            else:
                data = self._get_default_data_structure()

            # Ensure all required keys exist
            required_keys = [
                'total_tokens', 'total_cost', 'total_input_tokens', 'total_output_tokens',
                'monthly_usage', 'operations'
            ]
            for key in required_keys:
                if key not in data:
                    if key in ['monthly_usage', 'operations']:
                        data[key] = {} if key == 'monthly_usage' else []
                    else:
                        data[key] = 0

            return data
        except Exception as e:
            print(f"Error loading usage data: {e}")
            return self._get_default_data_structure()

    def _save_usage_data(self, data):
        """Save usage data to file"""
        try:
            with open(self.usage_file, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving usage data: {e}")

    def _get_default_data_structure(self):
        """Get default data structure"""
        return {
            'total_tokens': 0,
            'total_cost': 0.0,
            'total_input_tokens': 0,
            'total_output_tokens': 0,
            'monthly_usage': {},
            'operations': []
        }

    def optimize_prompt_for_tokens(self, prompt, max_tokens=4000):
        """
        Optimize prompt to stay within token limits

        Args:
            prompt: Original prompt
            max_tokens: Maximum tokens allowed

        Returns:
            str: Optimized prompt
        """
        # Simple optimization - truncate if too long
        # In a real implementation, this would use tiktoken for accurate counting
        estimated_tokens = len(prompt.split()) * 1.3  # Rough estimation

        if estimated_tokens > max_tokens:
            words = prompt.split()
            max_words = int(max_tokens / 1.3)
            optimized_prompt = ' '.join(words[:max_words])
            print(f"Optimized prompt from {len(words)} to {max_words} words")
            return optimized_prompt

        return prompt
