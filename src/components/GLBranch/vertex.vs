#version 300 es

// attribute vec2 coordinates;
// void main(void){
  
  //   gl_Position=vec4(coordinates,0.,1.);
  //   gl_PointSize=5.;
// }

float HueToRGB(float p,float q,float t){
  if(t<0.)t+=1.;
  if(t>1.)t-=1.;
  if(t<1./6.)return p+(q-p)*6.*t;
  if(t<1./2.)return q;
  if(t<2./3.)return p+(q-p)*(2./3.-t)*6.;
  return p;
}

vec4 hslToRGB(float h,float s,float l){
  float r,g,b;
  if(s==0.){
    r=l;
    g=l;
    b=l;
  }else{
    float q=l<.5?l*(1.+s):l+s-l*s;
    float p=2.*l-q;
    r=HueToRGB(p,q,h+1./3.);
    g=HueToRGB(p,q,h);
    b=HueToRGB(p,q,h-1./3.);
  }
  return vec4(r,g,b,1.);
}

vec4 toBezier(float u,vec4 P0,vec4 P1,vec4 P2,vec4 P3){
  // first level
  vec4 P01=mix(P0,P1,u);
  vec4 P02=mix(P1,P2,u);
  vec4 P03=mix(P2,P3,u);
  
  // second level
  vec4 P11=mix(P01,P02,u);
  vec4 P12=mix(P02,P03,u);
  
  // third level
  vec4 P21=mix(P11,P12,u);
  
  return P21;
}

uniform vec2 controllPoint[100];
uniform int numVerts;
uniform int numCps;
uniform vec2 resolution;

out vec4 color;

void main(){
  float u=float(numCps)*float(gl_VertexID)/float(numVerts);// goes from 0 to numCps
  float local_u=fract(u);// goes from 0 to 1
  // 4 controll points define one line segment
  // last point in each line segment is used as the first point in the next line segment
  int line_segment_index=int(floor(u)/4.);// goes from 0 to numCps/4
  float line_segment_u=fract(u/4.);// goes from 0.0 to 1.0 in one line segment (between 4 controll points)
  
  vec2 cp1=controllPoint[line_segment_index*4+0];
  vec2 cp2=controllPoint[line_segment_index*4+1];
  vec2 cp3=controllPoint[line_segment_index*4+2];
  vec2 cp4=controllPoint[line_segment_index*4+3];
  
  vec4 P0=toBezier(local_u,vec4(cp1,0.,1.),vec4(cp2,0.,1.),vec4(cp3,0.,1.),vec4(cp4,0.,1.));
  
  gl_Position=P0;
  gl_PointSize=8.;
  color=hslToRGB(local_u,1.,.5);
  
}