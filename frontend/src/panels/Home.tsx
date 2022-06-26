import React from "react";
import PropTypes from "prop-types";

import {
  Panel,
  PanelHeader,
  Header,
  Button,
  Group,
  Cell,
  Div,
  Avatar,
} from "@vkontakte/vkui";
import { UserInfo } from "@vkontakte/vk-bridge";

const Home = ({ id, go }: { id: string; go: (e: any) => void }) => (
  <Panel id={id}>
    <PanelHeader>Example</PanelHeader>

    <Group header={<Header mode="secondary">Navigation Example</Header>}>
      <Div>
        <Button
          stretched
          size="l"
          mode="secondary"
          onClick={go}
          data-to="persik"
        >
          Show me the Persik, please
        </Button>
      </Div>
    </Group>

    <div className="flex justify-center">kekfrrtg</div>
  </Panel>
);

Home.propTypes = {
  id: PropTypes.string.isRequired,
  go: PropTypes.func.isRequired,
  fetchedUser: PropTypes.shape({
    photo_200: PropTypes.string,
    first_name: PropTypes.string,
    last_name: PropTypes.string,
    city: PropTypes.shape({
      title: PropTypes.string,
    }),
  }),
};

export default Home;
