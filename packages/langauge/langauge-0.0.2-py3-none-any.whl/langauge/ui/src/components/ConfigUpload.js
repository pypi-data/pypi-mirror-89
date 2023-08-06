import React, { useState, useRef } from "react";
import { Button } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles((theme) => ({
  root: {
    "& > *": {
      margin: theme.spacing(1),
    },
  },
  input: {
    display: "none",
  },
}));

function ConfigUpload(props) {
  const classes = useStyles();
  const fileInput = useRef(null);
  const [hasFile, setHasFile] = useState(false);
  const [file, setFile] = useState("");

  const fileChange = (e) => {
    // Grabbing last 4 chars of filename AKA the type
    const fileType = e.target.value.slice(e.target.value.length - 5);
    if (fileType === ".json") {
      setHasFile(true);
      setFile(e.target.files[0].name);
    }
    // No characters = No file was uploaded.
    else if (fileType === "") {
      return;
    } else {
      alert("Input only accepts JSON files.");
    }
  };

  const clearFile = () => {
    setHasFile(false);
    setFile("");
    fileInput.current.value = null;
  };

  return (
    <div className={classes.root}>
      <input
        ref={fileInput}
        type="file"
        id="fetch-config-button"
        title="fetch selection"
        accept="application/JSON"
        onChange={(event) => {
          fileChange(event);
          props.fetchConfig(event);
        }}
        className={classes.input}
      />
      <div className="file-upload-label-container">
        <label className="file-upload-label" htmlFor="fetch-config-button">
          <Button variant="contained" component="span">
            {hasFile ? file : "Load Config"}
          </Button>
        </label>
        {hasFile && (
          <div>
            <i onClick={clearFile} className="fas fa-trash-alt"></i>
          </div>
        )}
      </div>
    </div>
  );
}

export default ConfigUpload;
