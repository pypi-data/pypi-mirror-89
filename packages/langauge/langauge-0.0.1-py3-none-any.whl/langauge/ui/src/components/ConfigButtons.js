import { GeneralControlsBar } from "./styled/GeneralControlsBar";
import React from "react";
import ConfigUpload from "./ConfigUpload";

class ConfigButtons extends React.Component {
  render() {
    return (
      <GeneralControlsBar>
        <ConfigUpload fetchConfig={this.props.fetchConfig} />
        <button
          className="button-generic"
          id="save-config-button"
          title="Save Current Config"
          onClick={(event) => this.props.saveConfig(event)}
        >
          <i className="fas fa-save" />
        </button>
        <button
          className="button-generic"
          id="run-config-button"
          title="Run All"
          onClick={(event) => this.props.runAll(event)}
        >
          <i className="fas fa-play" />
        </button>
      </GeneralControlsBar>
    );
  }
}

export default ConfigButtons;
