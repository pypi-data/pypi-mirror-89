import { Container } from "../styled-components";
import React from "react";

function Preview(props) {
  return (
    <Container className="custom-preview">
      <Container className="card-value text-small">
        <div className="previewDescription" id={"preview-" + props.formId}>
          <span>{props.preview}</span>
        </div>
      </Container>
    </Container>
  );
}

export default Preview;
