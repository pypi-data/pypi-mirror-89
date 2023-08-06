import { Container } from "./styled-components";
import LanLogo from "../assets/images/lanlogo.png";
import React from "react";
import Tabs from "./Tabs";

function NavBar(props) {
  return (
    <nav className="navbar navbar-expand-lg fixed-top ">
      <Container className="logo-header">
        <img src={LanLogo} alt="" />
        <h1>
          Lan<i>Gauge</i>
        </h1>
      </Container>
      <Container>
        <Tabs />
      </Container>
      <Container className="navbar-nav ml-auto">
        <Container className="user-detail-section">
          <span className="pr-2">Docs</span>
          <span className="pr-2">GitHub</span>
        </Container>
      </Container>
    </nav>
  );
}

export default NavBar;
