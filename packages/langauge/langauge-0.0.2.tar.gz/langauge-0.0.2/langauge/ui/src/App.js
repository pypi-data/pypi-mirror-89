import React, { Component } from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import Metrics from "./pages/Metrics";
import History from "./pages/History";
import Home from "./pages/Home.js";
import NavBar from "./components/NavBar";
import $ from "jquery";
import { ModelData } from "./data/ModelData";
import { TaskData } from "./data/TaskData";

const host = process.env.REACT_APP_BASE_URL;

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      channels: [
        {
          name: "A",
          file: null,
          task: "",
          model: "",
          taskId: "",
          availableModels: [],
          preview: "",
        },
        {
          name: "B",
          file: null,
          task: "",
          model: "",
          taskId: "",
          availableModels: [],
          preview: "",
        },
      ],
      availableTasks: [],
      time_taken: {},
    };
    this.addChannel = this.addChannel.bind(this);
    this.removeChannel = this.removeChannel.bind(this);
    this.handleTimeTakenChange = this.handleTimeTakenChange.bind(this);
    this.onTaskChange = this.onTaskChange.bind(this);
    this.onModelChange = this.onModelChange.bind(this);
    this.onFileChange = this.onFileChange.bind(this);

    this.runAll = this.runAll.bind(this);
    this.saveConfig = this.saveConfig.bind(this);
    this.fetchConfig = this.fetchConfig.bind(this);
    this.downloadFile = this.downloadFile.bind(this);
    this.disableButtons = this.disableButtons.bind(this);
    this.enableButtons = this.enableButtons.bind(this);
    this.update_preview = this.update_preview.bind(this);
    this.update_run = this.update_run.bind(this);
    this.runModel = this.runModel.bind(this);
    this.isValid = this.isValid.bind(this);
  }
  add;

  componentDidMount() {
    fetch(host + "/config/tasks")
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        let tasks = $.JSON.parse(data).map((task) => {
          return { value: task.value, display: task.label };
        });
        this.setState({
          availableTasks: [{ value: "", display: "(Select a Task)" }].concat(
            tasks
          ),
        });
      })
      .catch((error) => {
        let tasks = TaskData.map((task) => {
          return { value: task.value, display: task.label };
        });
        this.setState({
          availableTasks: [{ value: "", display: "(Select a Task)" }].concat(
            tasks
          ),
        });
      });
  }

  runModel(ev, type, numForm) {
    ev.preventDefault();
    const progressholder = "#progress-" + numForm;
    const { file, task, model } = this.state.channels[numForm];
    let endPoint = "";
    if (type === "preview") {
      endPoint = `/${task}/preview/${model}/5/${numForm}`;
    } else {
      endPoint = `/${task}/${model}/${numForm}`;
    }
    if (!this.isValid(numForm)) {
      alert("Please select all options.");
    } else {
      this.disableButtons(numForm);
      const div = $(
        '<div style="width:50px;display:flex;justify-content:center">' +
          '<div title="Processing.." class="spinner-border text-primary" style="width:32px;height:32px;margin:2px 0">' +
          "</div>" +
          "</div>"
      );
      const data = new FormData();
      data.append("file", file);
      $(progressholder).html(div);
      fetch(host + endPoint, {
        method: "POST",
        body: data,
      })
        .then((response) => response.json())
        .then((data) => {
          if (type === "preview") {
            this.update_preview(host + data, numForm, div[0]);
          } else {
            this.update_run(host + data, numForm, div[0]);
          }
        })
        .catch((error) => {
          $(div[0].childNodes[0]).replaceWith(
            '<i class="fas fa-exclamation-triangle" style="color:red;font-size:2rem;" title="Error Occurred"></i>'
          );
        });
    }
  }

  update_run(status_url, numForm, status_div) {
    // reference for inside of next lexical scope
    const that = this;
    // send GET request to status URL
    $.getJSON(status_url, function (data) {
      // update UI
      if (data["state"] !== "PENDING" && data["state"] !== "PROGRESS") {
        $(status_div.childNodes[0]).removeClass("spinner-border");
        if ("id" in data) {
          // show result
          $(status_div.childNodes[0]).replaceWith(
            '<i class="fas fa-check" style="color:green;font-size:2rem;" title="Success"></i>'
          );

          // updating channel task id
          let channels = [...that.state.channels];
          let channel = { ...channels[numForm] };
          channel.taskId = data["id"];
          channels[numForm] = channel;
          that.setState({ channels });

          that.handleTimeTakenChange(numForm, Number(data["time"]));
        } else {
          // something unexpected happened
          $(status_div.childNodes[0]).replaceWith(
            '<i class="fas fa-exclamation-triangle" style="color:red;font-size:2rem;" title="Error Occurred"></i>'
          );
        }
        that.enableButtons(numForm);
      } else {
        // rerun in 2 seconds

        setTimeout(() => {
          that.update_run(status_url, numForm, status_div);
        }, 10000);
      }
    });
  }

  update_preview(status_url, numForm, status_div) {
    // reference for inside of next lexical scope
    const that = this;
    // send GET request to status URL
    $.getJSON(status_url, function (data) {
      if (data["state"] !== "PENDING" && data["state"] !== "PROGRESS") {
        $(status_div.childNodes[0]).removeClass("spinner-border");
        if ("preview" in data) {
          // show result
          $(status_div.childNodes[0]).replaceWith(
            '<i class="fas fa-check" style="color:green;font-size:2rem;" title="Success"></i>'
          );

          // updating channel preview
          let channels = [...that.state.channels];
          let channel = { ...channels[numForm] };
          channel.preview = JSON.stringify(data["preview"]);
          channels[numForm] = channel;
          that.setState({ channels });
        }
        // something unexpected happened
        else {
          $(status_div.childNodes[0]).replaceWith(
            '<i class="fas fa-exclamation-triangle" style="color:red;font-size:2rem;" title="Error Occurred"></i>'
          );
        }
        that.enableButtons(numForm);
      } else {
        // rerun in 2 seconds
        setTimeout(() => {
          that.update_preview(status_url, numForm, status_div);
        }, 10000);
      }
    });
  }

  saveConfig(ev) {
    ev.preventDefault();
    const tasks = [];
    const models = [];
    this.state.channels.forEach((channel) => {
      if (channel.task !== "") tasks.push(channel.task);
      if (channel.model !== "") models.push(channel.model);
    });

    if (tasks.length !== models.length) {
      alert("Partial options cannot be saved.");
    } else {
      // console.log(this.state.file['file-0'].value);
      let data = JSON.stringify({
        // 'file': window.URL.createObjectURL(this.state.file['file-0']),
        tasks: tasks,
        models: models,
      });
      let bb = new Blob([data], { type: "application/json" });
      let a = document.createElement("a");
      a.download = "selection.json";
      a.href = window.URL.createObjectURL(bb);
      a.click();
    }
  }

  fetchConfig(ev) {
    ev.preventDefault();
    const reader = new FileReader();
    let selection_data = {};
    reader.onload = async (e) => {
      let text = e.target.result;
      if (typeof text !== "string") {
        return;
      }
      try {
        selection_data = JSON.parse(text);
      } catch (e) {
        return;
      }
      if (selection_data.models.length !== 0) {
        let jsonModels = selection_data.models;
        let jsonTasks = selection_data.tasks;

        // updating channel task and model syncronously

        for (let i = 0; i < jsonTasks.length; i++) {
          this.onTaskChange(i, jsonTasks[i]);
          this.onModelChange(i, jsonModels[i]);
        }
      }
    };

    reader.readAsText(ev.target.files[0]);
  }

  runAll(ev) {
    ev.preventDefault();
    this.state.channels.map((key, i) => {
      return this.runModel(ev, "run", i);
    });
  }

  downloadFile(ev, numForm) {
    ev.preventDefault();
    const taskId = this.state.channels[numForm].taskId;
    if (taskId === undefined) {
      alert("No file available for download.");
      return;
    }
    fetch(host + `/celery/fileDownload/${taskId}`, {
      method: "GET",
      headers: {
        "Content-Type": "text/csv",
      },
      responseType: "blob",
    })
      .then((response) => response.blob())
      .then((blob) => {
        let url = window.URL.createObjectURL(blob);
        let a = document.createElement("a");
        a.href = url;
        a.download = "results.txt";
        document.body.appendChild(a); // we need to append the element to the dom -> otherwise it will not work in firefox
        a.click();
        a.remove(); //afterwards we remove the element again
      });
  }

  isValid(numForm) {
    const { file, task, model } = this.state.channels[numForm];
    if (file === null || task === "" || model === "") {
      return false;
    } else {
      return true;
    }
  }

  disableButtons(numForm) {
    $("#channel-" + numForm + " *")
      .attr("disabled", "disabled")
      .off("click");
    $("#preview-button-" + numForm).css("pointer-events", "none");
    $("#run-button-" + numForm).css("pointer-events", "none");
    $("#download-button-" + numForm).css("pointer-events", "none");
  }

  enableButtons(numForm) {
    $("#channel-" + numForm + " *").removeAttr("disabled");
    $("#preview-button-" + numForm).removeAttr("style");
    $("#run-button-" + numForm).removeAttr("style");
    $("#download-button-" + numForm).removeAttr("style");
  }

  onFileChange(numForm, file) {
    // some shallow copy logic to avoid mutating state
    let channels = [...this.state.channels];
    let channel = { ...channels[numForm] };
    channel.file = file;
    channels[numForm] = channel;
    this.setState({ channels });
  }

  onTaskChange(numForm, value) {
    // some shallow copy logic to avoid mutating state
    let channels = [...this.state.channels];
    let channel = { ...channels[numForm] };
    channel.task = value;
    channels[numForm] = channel;
    this.setState({ channels });

    fetch(host + "/config/models/" + value)
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        let modelsFromApi = JSON.parse(data).models.map((model) => {
          return { value: model.value, display: model.label };
        });
        // updating our channel models
        let channels = [...this.state.channels];
        let channel = { ...channels[numForm] };
        channel.availableModels = modelsFromApi;
        channels[numForm] = channel;
        return this.setState({
          channels,
        });
      })
      .catch((error) => {
        if (value !== "ner") return;
        let modelsFromApi = ModelData.map((model) => {
          return { value: model.value, display: model.label };
        });
        // updating our channel models
        let channels = [...this.state.channels];
        let channel = { ...channels[numForm] };
        channel.availableModels = modelsFromApi;
        channels[numForm] = channel;
        return this.setState({
          channels,
        });
      });
  }

  onModelChange(numForm, value) {
    // some logic to avoid mutating state
    let channels = [...this.state.channels];
    let channel = { ...channels[numForm] };
    channel.model = value;
    channels[numForm] = channel;
    this.setState({ channels });
  }

  handleTimeTakenChange(numForm, time_taken) {
    this.setState({
      time_taken: {
        // object that we want to update
        ...this.state.time_taken, // keep all other key-value pairs
        [numForm]: time_taken,
      },
    });
  }

  addChannel() {
    const createChannel = (name) => {
      return {
        name: name,
        file: null,
        task: "",
        model: "",
        taskId: "",
        availableModels: [],
        preview: "",
      };
    };
    const length = this.state.channels.length;

    if (length === 1) {
      let channel = createChannel("B");
      this.setState({ channels: [...this.state.channels, channel] });
    } else if (length === 2) {
      let channel = createChannel("C");
      this.setState({ channels: [...this.state.channels, channel] });
    } else if (length === 3) {
      let channel = createChannel("D");
      this.setState({ channels: [...this.state.channels, channel] });
    }
  }

  removeChannel() {
    const length = this.state.channels.length;
    const filterChannels = (name) => {
      this.setState({
        channels: [...this.state.channels.filter((item) => item.name !== name)],
      });
    };

    if (length === 2) {
      filterChannels("B");
    }
    if (length === 3) {
      filterChannels("C");
    }
    if (length === 4) {
      filterChannels("D");
    }
  }

  render() {
    return (
      <>
        <Router>
          <NavBar />
          <Switch>
            <Route
              exact
              path="/"
              render={(props) => (
                <Home
                  channels={this.state.channels}
                  tasks={this.state.availableTasks}
                  time_taken={this.state.time_taken}
                  onTimeTakenChange={this.handleTimeTakenChange}
                  addChannel={this.addChannel}
                  removeChannel={this.removeChannel}
                  onModelChange={this.onModelChange}
                  onTaskChange={this.onTaskChange}
                  onFileChange={this.onFileChange}
                  runModel={this.runModel}
                  downloadFile={this.downloadFile}
                  runAll={this.runAll}
                  saveConfig={this.saveConfig}
                  fetchConfig={this.fetchConfig}
                />
              )}
            />
            <Route
              path="/metrics"
              render={(props) => (
                <Metrics
                  channels={this.state.channels}
                  time_taken={this.state.time_taken}
                />
              )}
            />
            <Route path="/history" component={History} />
          </Switch>
        </Router>
      </>
    );
  }
}

export default App;
