const prevMonths = [{m: 8, y: 2020}, {m: 9, y: 2020}, {m: 10, y: 2020}]
const calculateAverageHousePrice = (houses, month, year) => {
    let count = 0

    return houses.reduce((avg, houseData) => {
        const date = new Date(houseData.scraped_at)
        const scraped_at_year = date.getFullYear()
        const scraped_at_month = date.getMonth() + 1
        if (scraped_at_year === year && scraped_at_month === month)
            avg = (count * avg + houseData.price) / (++count)

        return avg
    }, 0)
}

(async () => {
    const res = await fetch("../data/data.json")
    const jsonData = await res.json()
    const lastScraped = jsonData.last_updated
    const averageHousePricePerMonth = prevMonths.map(({m, y}) => calculateAverageHousePrice(jsonData.entities, m, y))

    console.log({
        lastScraped,
        averageHousePricePerMonth
    })

    var ctx = document.getElementById('myChart').getContext('2d');
    var chart = new Chart(ctx, {
        // The type of chart we want to create
        type: 'line',
        // The data for our dataset
        data: {
            labels: ['Aug', 'Sep', 'Oct', 'Nov'],
            datasets: [{
                label: 'Average house price',
                backgroundColor: 'rgb(255, 99, 132)',
                borderColor: 'rgb(255, 99, 132)',
                data: averageHousePricePerMonth
            }]
        },
        // Configuration options go here
        options: {}
    });

})()