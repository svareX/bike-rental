from flask import Blueprint, request, flash, session, redirect, url_for, render_template
import matplotlib.pyplot as plt
import base64
import io

import auth
from service.statistics_service import StatisticsService

statistics = Blueprint('statistics', __name__)

@statistics.route('/statistics', methods=['GET', 'POST'])
@auth.login_required
@auth.employees_only
def page():
    userCount = StatisticsService.getUserCount()
    totalBikeRevenue = StatisticsService.getTotalBikeRevenue()
    mostRentedBike = StatisticsService.getMostRentedBike()
    mostRentedBrand = StatisticsService.getMostRentedBrand()
    totalNumberOfRents = StatisticsService.getTotalNumberOfRents()

    brand_rents = StatisticsService.getBrandRents()

    # Extract labels (brand names) and sizes (counts) from the result
    labels = [row[1] for row in brand_rents]  # Brand names
    sizes = [row[0] for row in brand_rents]   # Rent counts

    # Create the pie chart
    plt.figure(figsize=(6, 6), dpi=100)
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')

    # Save the chart to a temporary buffer
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png', bbox_inches='tight')
    plt.close()
    img_buf.seek(0)

    # Convert the image to base64 string
    chart_data = base64.b64encode(img_buf.getvalue()).decode('utf-8')

    return render_template(
        "statistics.jinja",
        chart_data=chart_data,  # Now passing the base64 encoded string
        labels=labels,
        sizes=sizes,
        userCount=userCount,
        totalBikeRevenue=totalBikeRevenue,
        mostRentedBike=mostRentedBike,
        mostRentedBrand=mostRentedBrand,
        totalNumberOfRents=totalNumberOfRents
    )