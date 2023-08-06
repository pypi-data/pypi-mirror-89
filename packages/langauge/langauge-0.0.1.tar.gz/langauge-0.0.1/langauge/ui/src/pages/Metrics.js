import React, { useState, useEffect } from "react";
import BarChart from "../components/BarChart";

function Metrics(props) {
  const [times, setTimes] = useState({});

  const populateEmptyIndices = (time_obj) => {
    const newTimes = { ...time_obj };
    const keys = Object.keys(newTimes);
    const maxKey = Math.max(keys);

    for (let i = 0; i < maxKey; i++) {
      if (!newTimes[i]) {
        newTimes[i] = 0;
      }
    }
    return newTimes;
  };

  // Populates Empty Indices When Props Change
  useEffect(() => {
    setTimes(populateEmptyIndices(props.time_taken));
  }, [props.time_taken]);

  return <BarChart channels={props.channels} data={times} />;
}

export default Metrics;
