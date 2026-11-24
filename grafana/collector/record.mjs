export function record(store, { type, data }) {
  switch (type) {
    case 'pageview':
      store.recordPageview(data || {});
      if (data?.sessionId) store.recordHeartbeat(data.sessionId);
      break;

    case 'heartbeat':
      if (data?.sessionId) store.recordHeartbeat(data.sessionId);
      break;

    case 'section_view':
      store.recordSectionView(data?.section);
      if (data?.dwellSeconds) store.recordSectionDwell(data.section, data.dwellSeconds);
      break;

    case 'section_dwell':
      store.recordSectionDwell(data?.section, data?.seconds);
      break;

    case 'scroll_depth':
      store.recordScrollDepth(data?.percent);
      break;

    case '3d_pose':
      store.record3DPose(data?.pose);
      break;

    case '3d_material':
      store.record3DMaterial(data?.mode);
      break;

    case 'click':
      store.recordClick(data?.target, data?.category);
      break;

    case 'form':
      store.recordFormEvent(data?.action);
      break;

    case 'web_vital':
      store.recordWebVital(typeof data?.name === 'string' ? data.name.toLowerCase() : null, data?.value);
      break;
  }
}
