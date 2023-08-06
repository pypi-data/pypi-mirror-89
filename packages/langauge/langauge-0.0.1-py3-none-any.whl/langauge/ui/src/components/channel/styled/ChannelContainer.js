import styled from "styled-components";

export const ChannelContainer = styled.div`
  border-top: 1px solid #bdbdbd;
  transition: 0.2s opacity ease-in;
`;

export const ChannelContainerInner = styled.div`
  width: 92%;
  display: grid;
  justify-content: space-between;
  justify-items: center;

  align-items: center;
  grid-template-columns: 5% 10% 15% 15% 45%;
  grid-template-rows: 250px;

  .fill-block {
    width: 50px;
  }

  @media (max-width: 1195px) {
    width: 100%;
    grid-template-rows: 300px;
  }
`;
