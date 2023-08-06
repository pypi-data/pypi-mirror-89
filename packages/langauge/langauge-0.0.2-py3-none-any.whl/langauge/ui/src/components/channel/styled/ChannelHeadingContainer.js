import styled from "styled-components";

// The full-width columns contain an extra 50px as a buffer
// due to the lower channels having a 50px wide button div on the right
export const ChannelHeadingContainer = styled.div`
  width: 92%;
  display: grid;
  justify-content: space-between;
  justify-items: center;
  align-items: center;
  grid-template-columns: 5% 10% 15% 15% 45%;
  grid-template-rows: 75px;

  @media (max-width: 1195px) {
    width: 100%;
  }
`;
