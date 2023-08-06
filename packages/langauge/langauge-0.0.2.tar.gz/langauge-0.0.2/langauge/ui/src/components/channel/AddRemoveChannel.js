import React from "react";
import "./AddRemoveChannel.css";

const AddRemoveChannel = ({ addChannel, removeChannel, channels }) => {
  return (
    <div className="channel-button-container">
      {channels.length !== 1 && (
        <div
          className="channel-button"
          title="Delete Channel"
          onClick={removeChannel}
        >
          <i className="fas fa-minus"></i>
        </div>
      )}
      {channels.length !== 4 && (
        <div
          className="channel-button"
          title="Add Channel"
          onClick={addChannel}
        >
          <i className="fas fa-plus"></i>
        </div>
      )}
    </div>
  );
};

export default AddRemoveChannel;
