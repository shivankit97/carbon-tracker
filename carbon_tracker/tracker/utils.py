import io
import base64
import matplotlib.pyplot as plt

def generate_chart_base64(data_dict):
    """
    Generates a bar chart from a dictionary, saves it to a BytesIO buffer,
    and returns it as a base64 encoded string.
    """
    if not data_dict:
        return None

    # Prevent GUI display
    plt.switch_backend('Agg')

    fig, ax = plt.subplots(figsize=(8, 5))

    categories = list(data_dict.keys())
    values = list(data_dict.values())

    ax.bar(categories, values, color=['#4e79a7', '#f28e2b', '#e15759', '#76b7b2'])

    ax.set_ylabel('CO2 Equivalent (kg)')
    ax.set_title('Carbon Footprint by Category')
    fig.tight_layout() # Adjust layout to make room for labels

    # Save plot to a BytesIO buffer
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)

    # Encode the buffer in base64
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')

    # Close the buffer and the plot
    buf.close()
    plt.close(fig)

    return image_base64

def generate_personalized_tips(data_dict):
    """
    Generates a list of personalized tips based on the category with the highest carbon footprint.
    """
    if not data_dict:
        return ["Start logging your activities to get personalized tips!"]

    # Find the category with the highest emissions
    highest_category = max(data_dict, key=data_dict.get).lower()

    tips = {
        'transport': "Your transport emissions are high. Consider carpooling, using public transport, or cycling for shorter trips.",
        'electricity': "Electricity usage is a major part of your footprint. Try switching to LED bulbs and unplugging devices when not in use.",
        'food': "Your diet has a significant impact. Reducing meat consumption, especially red meat, can lower your footprint.",
        'waste': "To reduce waste emissions, focus on recycling and composting. Avoid single-use plastics whenever possible."
    }

    # Return a list containing the most relevant tip
    return [tips.get(highest_category, "Keep up the great work on reducing your carbon footprint!")]

