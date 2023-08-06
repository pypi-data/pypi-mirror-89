import React, { useEffect, useState } from "react";
import FileUpload from "./FileUpload";
import TaskSelect from "./TaskSelect";
import ModelSelect from "./ModelSelect";
import Preview from "./Preview";
import Buttons from "./Buttons";
import {
  ChannelContainer,
  ChannelContainerInner,
} from "./styled/ChannelContainer";

const Channel = ({
  i,
  channel,
  tasks,
  onTaskChange,
  onModelChange,
  onFileChange,
  runModel,
  downloadFile,
}) => {
  const [opacity, setOpacity] = useState("0");

  useEffect(() => {
    setOpacity("1");
  }, []);

  return (
    <ChannelContainer
      id={"channel-" + i}
      className="container-fluid-side row"
      style={{ opacity: opacity }}
    >
      <ChannelContainerInner>
        <span className="channel-title-span">{channel.name}</span>
        <FileUpload
          formId={i}
          onFileChange={onFileChange}
          selectedFile={channel.file}
        />
        <TaskSelect
          formId={i}
          tasks={tasks}
          selectedTask={channel.task}
          onTaskChange={onTaskChange}
        />
        <ModelSelect
          formId={i}
          selectedModel={channel.model}
          models={channel.availableModels}
          onModelChange={onModelChange}
        />
        <Preview formId={i} preview={channel.preview} />
      </ChannelContainerInner>
      <Buttons formId={i} runModel={runModel} downloadFile={downloadFile} />
    </ChannelContainer>
  );
};

export default Channel;
