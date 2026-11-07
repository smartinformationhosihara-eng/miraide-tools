import React from 'react';
import {registerRoot, Composition, AbsoluteFill, useCurrentFrame, interpolate, spring, useVideoConfig} from 'remotion';
const Title = () => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const s = spring({frame: f, fps, config: {damping: 12}});
  return <AbsoluteFill style={{background:'linear-gradient(135deg,#ff8ad8,#7a5cff)',justifyContent:'center',alignItems:'center'}}>
    <div style={{fontSize:140,fontWeight:900,color:'#fff',transform:`scale(${s})`,fontFamily:'sans-serif'}}>MIRAIDE</div>
    <div style={{fontSize:56,color:'#fff',opacity:interpolate(f,[30,60],[0,1],{extrapolateRight:'clamp'})}}>Remotion テスト</div>
  </AbsoluteFill>;
};
const Root = () => <Composition id="Title" component={Title} durationInFrames={90} fps={30} width={1280} height={720}/>;
registerRoot(Root);
