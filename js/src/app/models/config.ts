import { IConfig } from './api';

// State is just IConfig with all fields optional
export type State = { [P in keyof IConfig]?: IConfig[P] };
