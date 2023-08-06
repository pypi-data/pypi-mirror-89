import { Container } from "../styled-components";
import React, { Component } from "react";

class ModelSelect extends Component {
  render() {
    return (
      <Container>
        <div id={"model-" + this.props.formId}>
          <select
            className="custom-select"
            value={this.props.selectedModel}
            onChange={(event) =>
              this.props.onModelChange(this.props.formId, event.target.value)
            }
          >
            {/* Have we selected our task yet? */}
            {this.props.models.length === 0 ? (
              <option defaultValue>(Select Task First)</option>
            ) : (
              <option defaultValue>(Select A Model)</option>
            )}
            {/* Mapping over available models */}
            {this.props.models &&
              this.props.models.map((model) => (
                <option key={model.value} value={model.value}>
                  {model.display}
                </option>
              ))}
          </select>
        </div>
      </Container>
    );
  }
}

export default ModelSelect;
