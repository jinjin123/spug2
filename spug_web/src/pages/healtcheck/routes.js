/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import { makeRoute } from "../../libs/router";
import Healtcheck from './healtcheck/index';


export default [
makeRoute('/check', Healtcheck),
]