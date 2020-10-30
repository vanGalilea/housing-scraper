const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]
const prevMonths = [{m: 8, y: 2020}, {m: 9, y: 2020}, {m: 10, y: 2020}]
const calculateAverageHousePrice = (houses, month, year, livingArea) => {
    let count = 0

    return houses.reduce((avg, houseData) => {
        const areaMargin = 5
        let inSizeRange = true
        const date = new Date(houseData.scraped_at)
        const scraped_at_year = date.getFullYear()
        const scraped_at_month = date.getMonth() + 1
        if (livingArea) {
            const diffrence = Math.abs(livingArea - houseData.living_area)
            inSizeRange = areaMargin >= diffrence && diffrence >= 0
        }
        if (inSizeRange && scraped_at_year === year && scraped_at_month === month) avg = (count * avg + houseData.price) / (++count)

        return avg
    }, 0)
}

(async () => {
    const res = await fetch("../data/data.json")
    const jsonData = await res.json()
    const lastScraped = jsonData.last_updated
    const averageHousePricePerMonthAll = prevMonths.map(({m, y}) => calculateAverageHousePrice(jsonData.entities, m, y))
    const averageHousePricePerMonthS = prevMonths.map(({m, y}) => calculateAverageHousePrice(jsonData.entities, m, y, 115))
    const averageHousePricePerMonthM = prevMonths.map(({m, y}) => calculateAverageHousePrice(jsonData.entities, m, y, 125))
    const averageHousePricePerMonthL = prevMonths.map(({m, y}) => calculateAverageHousePrice(jsonData.entities, m, y, 135))
    const averageHousePricePerMonthXL = prevMonths.map(({m, y}) => calculateAverageHousePrice(jsonData.entities, m, y, 145))

    const labels = prevMonths.map(({m, y}) => `${monthNames[m - 1]}-${y}`)

    var chart1 = document.getElementById('chart1').getContext('2d');
    new Chart(chart1, {
        type: 'line',
        data: {
            labels,
            datasets: [{
                label: 'Avg. price ofa all houses',
                backgroundColor: 'rgb(255, 99, 132)',
                borderColor: 'rgb(255, 99, 132)',
                data: averageHousePricePerMonthAll
            }]
        },
    })

    var chart2 = document.getElementById('chart2').getContext('2d');
    new Chart(chart2, {
        type: 'line',
        data: {
            labels,
            datasets: [{
                label: 'Avg. price house (110-120m2)',
                backgroundColor: 'rgb(255, 99, 132)',
                borderColor: 'rgb(255, 99, 132)',
                data: averageHousePricePerMonthS
            }]
        },
    })
    var chart3 = document.getElementById('chart3').getContext('2d');
    new Chart(chart3, {
        type: 'line',
        data: {
            labels,
            datasets: [{
                label: 'Avg. price house (120-130m2)',
                backgroundColor: 'rgb(255, 99, 132)',
                borderColor: 'rgb(255, 99, 132)',
                data: averageHousePricePerMonthM
            }]
        },
    })
    var chart4 = document.getElementById('chart4').getContext('2d');
    new Chart(chart4, {
        type: 'line',
        data: {
            labels,
            datasets: [{
                label: 'Avg. price house (130-140m2)',
                backgroundColor: 'rgb(255, 99, 132)',
                borderColor: 'rgb(255, 99, 132)',
                data: averageHousePricePerMonthL
            }]
        },
    })
     var chart5 = document.getElementById('chart5').getContext('2d');
    new Chart(chart5, {
        type: 'line',
        data: {
            labels,
            datasets: [{
                label: 'Avg. price house (140-150m2)',
                backgroundColor: 'rgb(255, 99, 132)',
                borderColor: 'rgb(255, 99, 132)',
                data: averageHousePricePerMonthXL
            }]
        },
    })

})()