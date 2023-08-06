import React, { useState, useRef } from "react";
import { Button } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";
import "./FileUpload.css";
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

function FileUpload(props) {
  const classes = useStyles();
  const fileInput = useRef(null);
  const [hasFile, setHasFile] = useState(props.selectedFile ? true : false);
  const [file, setFile] = useState(
    props.selectedFile ? props.selectedFile.name : ""
  );

  const fileChange = (e) => {
    // Grabbing last 4 chars of filename AKA the type
    const fileType = e.target.value.slice(e.target.value.length - 4);
    if (fileType === ".txt") {
      setHasFile(true);
      setFile(e.target.files[0].name);
    }
    // No characters = No file was uploaded.
    else if (fileType === "") {
      return;
    } else {
      alert("Input only accepts text files.");
    }

    // update file property under channel state
    props.onFileChange(props.formId, fileInput.current.files[0]);
  };

  const clearFile = () => {
    setHasFile(false);
    setFile("");
    props.onFileChange(props.formId, null);
  };

  return (
    <div className={classes.root}>
      <input
        ref={fileInput}
        type="file"
        id={"file-" + props.formId}
        onChange={fileChange}
        name="myfile"
        accept=".txt"
        className={classes.input}
      />
      <div className="file-upload-label-container">
        <label className="file-upload-label" htmlFor={"file-" + props.formId}>
          <Button variant="contained" component="span" size="small">
            {hasFile ? file : "Select File"}
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

export default FileUpload;
