import React, { Component } from "react";
import { DataGrid } from "@material-ui/data-grid";
import Grid from "@material-ui/core/Grid";
import "./History.css";

const columns = [
  { field: "id", headerName: "ID", width: 325 },
  { field: "task", headerName: "TASK", width: 125 },
  { field: "model", headerName: "MODEL", width: 300 },
  { field: "status", headerName: "STATUS", width: 125 },
  {
    field: "date_done",
    headerName: "COMPLETION TIME",
    type: "date",
    width: 225,
  },
];

const host = process.env.REACT_APP_BASE_URL;

export default class History extends Component {
  state = {
    setSelection: "",
    rows: [],
    filterBy: "",
  };

  componentDidMount() {
    fetch(host + "/celery/history?page_size=7&page_num=1")
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        this.setState({
          rows: data,
        });
      })
      .catch((error) => {
        console.log(error);
      });
  }

  downloadFile() {
    if (this.state.setSelection === "") {
      alert("Please select a record.");
      return;
    }
    fetch(host + `/celery/fileDownload/${this.state.setSelection}`, {
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

  handleInput(e) {
    this.setState({
      filterBy: e.target.value,
    });
  }

  render() {
    // This performs a client-side filter search on all
    // the history rows
    const viewRows = this.state.rows.filter((row) => {
      if (row.id.includes(this.state.filterBy)) return true;
      if (row.model.includes(this.state.filterBy)) return true;
      if (row.date_done.includes(this.state.filterBy)) return true;
      else return false;
    });
    return (
      <div className="history-container">
        <div className="history-header">
          <button
            className="button-generic"
            title="Download"
            onClick={() => this.downloadFile()}
          >
            <i className="fas fa-download" />
          </button>
          <input
            type="text"
            className="form-control"
            onChange={(e) => this.handleInput(e)}
            value={this.state.filterBy}
            placeholder="Search.."
          />
        </div>
        <Grid style={{ height: 490, backgroundColor: "white" }}>
          <DataGrid
            rows={viewRows}
            columns={columns}
            pageSize={7}
            checkboxSelection
            onSelectionChange={(newSelection) => {
              this.setState({
                setSelection: newSelection.rowIds,
              });
            }}
          />
        </Grid>
      </div>
    );
  }
}
