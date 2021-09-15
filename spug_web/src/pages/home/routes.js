/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import { lazy } from 'react';
import { makeRoute } from 'libs/router';

export default [
  makeRoute('', lazy(() => import('./index'))),
]
