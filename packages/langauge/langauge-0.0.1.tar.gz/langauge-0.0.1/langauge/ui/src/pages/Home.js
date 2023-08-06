import React, { Component } from "react";
import { Container } from "../components/styled-components";

import ColHeadings from "../components/channel/ColHeadings.js";
import Channel from "../components/channel/Channel.js";
import AddRemoveChannel from "../components/channel/AddRemoveChannel";
import ConfigButtons from "../components/ConfigButtons";

import "./Home.css";

class Home extends Component {
  render() {
    const channels = this.props.channels;
    return (
      <>
        <Container className="home-container">
          <ConfigButtons
            saveConfig={this.props.saveConfig}
            fetchConfig={this.props.fetchConfig}
            runAll={this.props.runAll}
          />
          <div className="channel-container">
            <ColHeadings />
            {channels.map((channel, i) => (
              <Channel
                i={i}
                key={i}
                channel={channel}
                tasks={this.props.tasks}
                onTaskChange={this.props.onTaskChange}
                onModelChange={this.props.onModelChange}
                runModel={this.props.runModel}
                downloadFile={this.props.downloadFile}
                onFileChange={this.props.onFileChange}
              />
            ))}
          </div>
        </Container>
        <AddRemoveChannel
          addChannel={this.props.addChannel}
          removeChannel={this.props.removeChannel}
          channels={channels}
        />
      </>
    );
  }
}

export default Home;
