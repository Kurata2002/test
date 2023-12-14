'use strict'


const mapHeight = 20;
const mapWidth = 40;
const maxVal = 741;  // 追加

//タブの変換
function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].classList.remove("active");
    }

    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.classList.add("active");

    // タブが切り替わったときにグラフを描画する関数を呼び出す
    if (tabName === 'Tab2') {
        drawSampleChart();
    }
}

function drawCO2Chart() {
    var chartColors = {
        red: 'rgb(255, 99, 132)',
    };

    var ctx = document.getElementById('CO2Chart').getContext('2d');
    var chart = new Chart(ctx, {
        type: 'line',
        data: {
            datasets: [{
                label: 'CO2',
                borderColor: chartColors.red,
                fill: false,
                data: []
            }]
        },
        options: {
            legend: {
                position: 'bottom'
            },
            scales: {
                x: {
                    type: 'realtime',
                    realtime: {
                        delay: 1000, // 1秒おきに更新
                        onRefresh: function (chart) {
                            const url = 'http://localhost:3000/';  // サーバーのエンドポイントを指定

                            // サーバーからデータを取得
                            fetch(url, { method: 'get' })
                                .then(response => response.json())
                                .then(data => {
                                    console.log(data);

                                    // 新しいデータをデータセットに追加
                                    chart.data.datasets[0].data.push({
                                        x: Date.now(), // 現在のタイムスタンプ
                                        y: data.CO2 // 取得したCO2データ
                                    });

                                    // 表示データ点の数を制限してパフォーマンスを向上させる
                                    const maxDataPoints = 50;
                                    while (chart.data.datasets[0].data.length > maxDataPoints) {
                                        chart.data.datasets[0].data.shift(); // 古いデータを削除
                                    }


                                    sleep(10000);  // 10秒間プログラムを停止

                                    // チャートを更新
                                    chart.update()
                                })
                                .catch(error => {
                                    console.error('Error fetching data:', error);
                                });
                        }
                    }
                }
            }
        }
    });
}

function drawAQIChart() {
    var chartColors = {
        blue: 'rgb(54, 162, 235)',
    };

    var ctx = document.getElementById('AQIChart').getContext('2d');
    var chart = new Chart(ctx, {
        type: 'line',
        data: {
            datasets: [{
                label: 'AQI',
                borderColor: chartColors.blue,
                fill: false,
                cubicInterpolationMode: 'monotone',
                data: []
            }]
        },
        options: {
            legend: {
                position: 'bottom'
            },
            scales: {
                x: {
                    type: 'realtime',
                    realtime: {
                        delay: 1000,
                        onRefresh: function (chart) {
                            const url = 'http://localhost:3000/';  // サーバーのエンドポイントを指定

                            // サーバーからデータを取得
                            fetch(url, { method: 'get' })
                                .then(response => response.json())
                                .then(data => {
                                    console.log(data);

                                    // Add the new data to the dataset
                                    chart.data.datasets[0].data.push({
                                        x: Date.now(),
                                        y: data.AQI
                                    });

                                    // Limit the number of data points displayed to improve performance
                                    const maxDataPoints = 50;
                                    while (chart.data.datasets[0].data.length > maxDataPoints) {
                                        chart.data.datasets[0].data.shift();
                                    }

                                    // Update the chart
                                    chart.update();
                                })
                                .catch(error => {
                                    console.error('Error fetching data:', error);
                                });
                        }
                    }
                }
            }
        }
    });
}

function drawTVOCChart() {
    var chartColors = {
        yellow: 'rgb(255, 205, 86)',
    };

    var ctx = document.getElementById('TVOCChart').getContext('2d');
    var chart = new Chart(ctx, {
        type: 'line',
        data: {
            datasets: [{
                label: 'TVOC',
                borderColor: chartColors.yellow,
                fill: false,
                cubicInterpolationMode: 'monotone',
                data: []
            }]
        },
        options: {
            legend: {
                position: 'bottom'
            },
            scales: {
                x: {
                    type: 'realtime',
                    realtime: {
                        delay: 1000,
                        onRefresh: function (chart) {
                            const url = 'http://localhost:3000/';  // サーバーのエンドポイントを指定

                            // サーバーからデータを取得
                            fetch(url, { method: 'get' })
                                .then(response => response.json())
                                .then(data => {
                                    console.log(data);

                                    // Add the new data to the dataset
                                    chart.data.datasets[0].data.push({
                                        x: Date.now(),
                                        y: data.TVOC
                                    });

                                    // Limit the number of data points displayed to improve performance
                                    const maxDataPoints = 50;
                                    while (chart.data.datasets[0].data.length > maxDataPoints) {
                                        chart.data.datasets[0].data.shift();
                                    }

                                    // Update the chart
                                    chart.update();
                                })
                                .catch(error => {
                                    console.error('Error fetching data:', error);
                                });
                        }
                    }
                }
            }
        }
    });
}

// 各グラフを描画
drawCO2Chart();
drawAQIChart();
drawTVOCChart();



document.addEventListener("DOMContentLoaded", function () {
    var elm = document.getElementById('test_line');

    // 初回の実行
    fetchDataAndTest(elm);

    // 5秒ごとにデータを取得し、テスト関数を呼び出す
    setInterval(function () {
        fetchDataAndTest(elm);
    }, 5000);
});

function fetchDataAndTest(elm) {
    const url = 'http://localhost:3000/';  // サーバーのエンドポイントを指定

    // サーバーからデータを取得
    fetch(url, { method: 'get' })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            test(elm, data); // データを渡してテスト関数を呼び出す
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
}

function test(elm, data) {
    if (data.CO2 > 1500) {
        elm.textContent = 'ひどい';
        elm.style.background = '#ff9999'; // 赤色
    } else if (data.CO2 >= 1000) {
        elm.textContent = '悪い';
        elm.style.background = '#ffcccc'; // ピンク色
    } else if (data.CO2 >= 800) {
        elm.textContent = '中程度';
        elm.style.background = '#ffffcc'; // 黄色
    } else if (data.CO2 >= 600) {
        elm.textContent = '良い';
        elm.style.background = '#ccffcc'; // 緑色
    } else {
        elm.textContent = '優れている';
        elm.style.background = '#99ff99'; // 青色
    }
}



function drawHeatmap() {
    window.onload = function () {
        // ヘルパー関数
        function $(id) {
            return document.getElementById(id);
        };

        /* レジェンドコード */
        // グラデーションを表示したいので描画する必要があります
        var legendCanvas = document.createElement('canvas');
        legendCanvas.width = 100;
        legendCanvas.height = 10;

        var legendCtx = legendCanvas.getContext('2d');
        var gradientCfg = {};

        function updateLegend(heatmapdata) {
            // onExtremaChangeコールバックは最小値、最大値、およびグラデーション設定を提供してくれるので、レジェンドを更新できます
            $('min').innerHTML = heatmapdata.min;
            $('max').innerHTML = heatmapdata.max;
            // グラデーション画像を再生成
            if (heatmapdata.gradient != gradientCfg) {
                gradientCfg = heatmapdata.gradient;
                var gradient = legendCtx.createLinearGradient(0, 0, 100, 1);
                for (var key in gradientCfg) {
                    gradient.addColorStop(key, gradientCfg[key]);
                }

                legendCtx.fillStyle = gradient;
                legendCtx.fillRect(0, 0, 100, 10);
                $('gradient').src = legendCanvas.toDataURL();
            }
        };
        /* レジェンドコード終了 */


        // ヒートマップのインスタンスを作成
        var heatmap = h337.create({
            container: document.getElementById('heatmapContainer'),
            maxOpacity: .5,
            radius: 10,
            blur: .75,
            // extremaが変更されるたびにレジェンドを更新
            onExtremaChange: function onExtremaChange(heatmapdata) {
                updateLegend(heatmapdata);
            }
        });

        // データ生成のための境界
        var width = (+window.getComputedStyle(document.body).width.replace(/px/, ''));
        var height = (+window.getComputedStyle(document.body).height.replace(/px/, ''));

        // 1000のデータポイントを生成
        var generate = function () {
            // ランダムに極値を生成
            var extremas = [(Math.random() * 1000) >> 0, (Math.random() * 1000) >> 0];
            var max = Math.max.apply(Math, extremas);
            var min = Math.min.apply(Math, extremas);
            var t = [];

            for (var i = 0; i < 1000; i++) {
                var x = (Math.random() * width) >> 0;
                var y = (Math.random() * height) >> 0;
                var c = ((Math.random() * max - min) >> 0) + min;
                // ちなみに、各ポイントに半径を設定できます
                var r = (Math.random() * 80) >> 0;
                // データセットに追加
                t.push({ x: x, y: y, value: c, radius: r });
            }
            var init = +new Date;
            // 生成されたデータセットを設定
            heatmap.setData({
                min: min,
                max: max,
                heatmapdata: t
            });
            console.log('took ', (+new Date) - init, 'ms');
        };
        // 最初に生成
        generate();

        // ユーザーがContainerWrapperをクリックするたびにデータが再生成されます -> 新しい最大値と最小値
        document.getElementById('heatmapContainerWrapper').onclick = function () { generate(); };
    };
}
