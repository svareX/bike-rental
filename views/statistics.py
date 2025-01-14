import base64
import io

import matplotlib.pyplot as plt
from flask import Blueprint, render_template

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

    labels = [row[1] for row in brand_rents]
    sizes = [row[0] for row in brand_rents]

    plt.figure(figsize=(6, 6), dpi=100)
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')

    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png', bbox_inches='tight')
    plt.close()
    img_buf.seek(0)

    chart_data = base64.b64encode(img_buf.getvalue()).decode('utf-8')

    return render_template(
        "statistics.jinja",
        chart_data=chart_data,
        labels=labels,
        sizes=sizes,
        userCount=userCount,
        totalBikeRevenue=totalBikeRevenue,
        mostRentedBike=mostRentedBike,
        mostRentedBrand=mostRentedBrand,
        totalNumberOfRents=totalNumberOfRents
    )