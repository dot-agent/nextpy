import { GuiClient } from 'api';
import { atom } from 'recoil';

export const clientState = atom<GuiClient>({
  key: 'Client',
  default: new GuiClient()
});
