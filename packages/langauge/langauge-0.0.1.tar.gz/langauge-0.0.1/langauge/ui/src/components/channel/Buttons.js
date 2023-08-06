import { Container } from "../styled-components";
import "./Buttons.css";
import React from "react";

function Buttons(props) {
  return (
    <Container>
      <div className="buttons-div">
        <div id={"progress-" + props.formId}></div>

        <button
          className="button-generic"
          id={"preview-button-" + props.formId}
          title="Generate Preview"
          onClick={(event) => props.runModel(event, "preview", props.formId)}
        >
          <i className="fas fa-border-style" />
        </button>

        <button
          className="button-generic"
          id={"run-button-" + props.formId}
          title="Run"
          onClick={(event) => props.runModel(event, "main", props.formId)}
        >
          <i className="far fa-play-circle"></i>
        </button>

        <button
          className="button-generic"
          id={"download-button-" + props.formId}
          title="Download"
          onClick={(event) => props.downloadFile(event, props.formId)}
        >
          <i className="fas fa-download" />
        </button>
      </div>
    </Container>
  );
}

export default Buttons;
