import React from "react";
import { Container } from "../styled-components";
import { ChannelHeadingContainer } from "./styled/ChannelHeadingContainer";
import "./ColHeadings.css";
function ColHeadings() {
  return (
    <div className="column-header">
      <ChannelHeadingContainer className="container-fluid-side row">
        <Container className="card-heading is-light-text ">
          {/* Div To Align Columns Properly */}
          <div />
        </Container>
        <Container className="card-heading is-light-text ">
          <h2 className="is-dark-text-light letter-spacing text-medium">
            Data
          </h2>
        </Container>
        <Container className="card-heading is-light-text ">
          <h2 className="is-dark-text-light letter-spacing text-medium">
            Task
          </h2>
        </Container>
        <Container className="card-heading is-light-text ">
          <h2 className="is-dark-text-light letter-spacing text-medium">
            Model
          </h2>
        </Container>
        <Container className="card-heading is-light-text ">
          <h2 className="is-dark-text-light letter-spacing text-medium">
            Preview
          </h2>
        </Container>
      </ChannelHeadingContainer>
      {/* Div To Emulate Buttons Div */}
      <div className="fill-block" />
    </div>
  );
}

export default ColHeadings;
