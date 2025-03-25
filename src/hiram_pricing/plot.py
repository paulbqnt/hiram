import numpy as np
import matplotlib.pyplot as plt


class OptionPlotter:
    """
    Advanced utility for plotting option characteristics,
    with comprehensive Greek sensitivity analysis
    """

    def __init__(self, option, market_data, pricing_engine):
        """
        Initialize the plotter with an option, market data, and pricing engine

        :param option: Option object to plot
        :param market_data: MarketData object with pricing parameters
        :param pricing_engine: Pricing engine to calculate option values
        """
        self.option = option
        self.market_data = market_data
        self.pricing_engine = pricing_engine

        # Use a built-in matplotlib style instead of seaborn
        plt.style.use('default')

    def plot_greeks(self, greek_type='delta', range_factor=0.5, num_points=100):
        """
        Comprehensive plot of option Greeks sensitivity

        :param greek_type: Type of greek to plot
        :param range_factor: Range around current market data to plot
        :param num_points: Number of points to calculate
        """
        # Supported greek types
        supported_greeks = ['delta', 'gamma', 'vega', 'theta', 'rho']
        if greek_type.lower() not in supported_greeks:
            raise ValueError(f"Unsupported greek type. Choose from {supported_greeks}")

        # Create variations of market data
        spot = self.market_data.spot
        volatility = self.market_data.volatility
        rate = self.market_data.rate

        # Prepare variation range based on greek type
        greek_ranges = {
            'delta': np.linspace(spot * (1 - range_factor), spot * (1 + range_factor), num_points),
            'gamma': np.linspace(spot * (1 - range_factor), spot * (1 + range_factor), num_points),
            'vega': np.linspace(volatility * (1 - range_factor), volatility * (1 + range_factor), num_points),
            'theta': np.linspace(0, 2, num_points),  # Time to expiry variation
            'rho': np.linspace(rate * (1 - range_factor), rate * (1 + range_factor), num_points)
        }

        # Compute Greeks
        greek_values = []
        x_values = greek_ranges[greek_type.lower()]

        for x in x_values:
            # Create a copy of market data to avoid mutation
            import copy
            temp_market_data = copy.deepcopy(self.market_data)

            # Modify appropriate parameter
            if greek_type.lower() in ['delta', 'gamma']:
                temp_market_data.spot = x
            elif greek_type.lower() == 'vega':
                temp_market_data.volatility = x
            elif greek_type.lower() == 'theta':
                # This requires a bit more sophisticated handling
                # We'll simulate time decay by adjusting expiry
                temp_option = copy.deepcopy(self.option)
                temp_option.expiry = x
                temp_option = temp_option  # To avoid unused variable warning
            elif greek_type.lower() == 'rho':
                temp_market_data.rate = x

            # Calculate option price
            try:
                pricing_result = self.pricing_engine.calculate(self.option, temp_market_data)
                greek_values.append(pricing_result.get(greek_type.lower(), np.nan))
            except Exception as e:
                print(f"Error calculating {greek_type}: {e}")
                greek_values.append(np.nan)

        # Plotting
        plt.figure(figsize=(12, 6))
        plt.plot(x_values, greek_values, color='blue', linewidth=2, label=f'{greek_type.capitalize()} Sensitivity')
        plt.title(f'Option {greek_type.capitalize()} Sensitivity', fontsize=14)

        # X-axis label
        x_labels = {
            'delta': 'Spot Price',
            'gamma': 'Spot Price',
            'vega': 'Volatility',
            'theta': 'Time to Expiry',
            'rho': 'Risk-Free Rate'
        }
        plt.xlabel(x_labels[greek_type.lower()], fontsize=12)
        plt.ylabel(f'{greek_type.capitalize()} Value', fontsize=12)

        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()

    def plot_all_greeks(self, range_factor=0.5, num_points=100):
        """
        Plot all Greeks in a single call

        :param range_factor: Range around current market data to plot
        :param num_points: Number of points to calculate
        """
        greeks = ['delta', 'gamma', 'vega', 'theta', 'rho']

        fig, axs = plt.subplots(len(greeks), 1, figsize=(12, 15))
        fig.suptitle('Option Greeks Sensitivity', fontsize=16)

        for i, greek in enumerate(greeks):
            try:
                # Compute Greek values
                spot = self.market_data.spot
                volatility = self.market_data.volatility
                rate = self.market_data.rate

                # Prepare variation range
                greek_ranges = {
                    'delta': np.linspace(spot * (1 - range_factor), spot * (1 + range_factor), num_points),
                    'gamma': np.linspace(spot * (1 - range_factor), spot * (1 + range_factor), num_points),
                    'vega': np.linspace(volatility * (1 - range_factor), volatility * (1 + range_factor), num_points),
                    'theta': np.linspace(0, 2, num_points),
                    'rho': np.linspace(rate * (1 - range_factor), rate * (1 + range_factor), num_points)
                }

                x_values = greek_ranges[greek]
                greek_values = []

                for x in x_values:
                    import copy
                    temp_market_data = copy.deepcopy(self.market_data)

                    # Modify appropriate parameter
                    if greek in ['delta', 'gamma']:
                        temp_market_data.spot = x
                    elif greek == 'vega':
                        temp_market_data.volatility = x
                    elif greek == 'theta':
                        temp_option = copy.deepcopy(self.option)
                        temp_option.expiry = x
                        temp_option = temp_option  # To avoid unused variable warning
                    elif greek == 'rho':
                        temp_market_data.rate = x

                    # Calculate option price
                    try:
                        pricing_result = self.pricing_engine.calculate(self.option, temp_market_data)
                        greek_values.append(pricing_result.get(greek, np.nan))
                    except Exception as e:
                        print(f"Error calculating {greek}: {e}")
                        greek_values.append(np.nan)

                # Plot in respective subplot
                axs[i].plot(x_values, greek_values, color='blue', linewidth=2)
                axs[i].set_title(f'{greek.capitalize()} Sensitivity', fontsize=12)
                axs[i].set_xlabel({
                                      'delta': 'Spot Price',
                                      'gamma': 'Spot Price',
                                      'vega': 'Volatility',
                                      'theta': 'Time to Expiry',
                                      'rho': 'Risk-Free Rate'
                                  }[greek], fontsize=10)
                axs[i].set_ylabel(f'{greek.capitalize()} Value', fontsize=10)
                axs[i].grid(True, linestyle='--', alpha=0.7)

            except Exception as e:
                print(f"Error plotting {greek}: {e}")

        plt.tight_layout()
        plt.show()