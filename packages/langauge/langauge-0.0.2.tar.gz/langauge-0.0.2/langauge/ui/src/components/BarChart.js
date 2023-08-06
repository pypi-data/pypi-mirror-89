import React from "react";
import { Bar, defaults } from "react-chartjs-2";
import { Container } from "./styled-components";

function dynamicColors() {
  let r = Math.floor(Math.random() * 255);
  let g = Math.floor(Math.random() * 255);
  let b = Math.floor(Math.random() * 255);
  return "rgba(" + r + "," + g + "," + b + ")";
}

function poolColors(a) {
  let pool = [];
  for (let i = 0; i < a; i++) {
    pool.push(dynamicColors());
  }
  return pool;
}

function BarChart(props) {
  // Default Styles To Pass Down To Bar Children
  defaults.global.defaultFontFamily = "Trebuchet MS";
  defaults.global.defaultFontColor = "#242424";
  defaults.global.defaultFontSize = 24;

  const options = {
    legend: {
      labels: {
        fontSize: 20,
      },
    },
    scales: {
      yAxes: [
        {
          scaleLabel: {
            display: true,
            labelString: "Time",

            fontSize: 20,
          },
          ticks: {},
        },
      ],
      xAxes: [
        {
          scaleLabel: {
            display: true,
            labelString: "Channel",
            fontSize: 20,
          },
          ticks: {
            fontSize: 20,
          },
        },
      ],
    },
    tooltips: {
      callbacks: {
        label: function (t, d) {
          let xLabel = d.datasets[t.datasetIndex].label;
          let yLabel = d.datasets[t.datasetIndex].data[t.index];
          return xLabel + ": " + yLabel;
        },
      },
    },
  };

  let labels = props.channels.map((channel) => channel.name);

  const time_state = {
    labels: labels,
    datasets: [
      {
        label: "Execution Time",
        backgroundColor: poolColors(Object.keys(props.data).length),
        data: Object.values(props.data),
      },
    ],
  };

  return (
    <Container className="container-fluid-side row ">
      <Container
        className="container-fluid-side row"
        style={{ height: "500px" }}
      >
        <div>
          <Bar data={time_state} options={options} height={600} width={900} />
        </div>
      </Container>
      {/*<Container className="container-fluid-side row custom-row">*/}
      {/*    <Bar data={acc_state} options={options}/>*/}
      {/*</Container>*/}
    </Container>
  );
}

export default BarChart;
