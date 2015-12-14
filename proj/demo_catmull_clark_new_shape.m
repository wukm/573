function demo_catmull_clark
% graphical interface for modified 
% catmull-clark subdivision

% Initialize data
global AMB_Data;
AMB_Data=[];

% Initialize GUI
clf reset;
% Text for title
uicontrol('Units','normalized', ...
  	'BackgroundColor',get(gcf,'Color'), ...
	'HorizontalAlignment','center', ...
        'FontWeight','bold',...
        'FontSize',20,...
	'Position',[.05,.91,.9,.07],...
	'String','Catmull-Clark Subdivision',...
	'Style','text');

% Text for alpha
AMB_Data.uicontrols(1)=uicontrol('Units','normalized', ...
	'BackgroundColor',get(gcf,'Color'), ...
	'HorizontalAlignment','left', ...
	'Position',[.5,.85,.3,.05],...
	'String','alpha=1.5000', ...
	'Style','text');

% Slider for alpha
AMB_Data.uicontrols(2)=uicontrol('Units','normalized', ...
	'BackgroundColor',get(gcf,'Color'), ...
	'Position',[.05,.85,.4,.05], ...
	'Min',-2,'Max',2,'Value',1.5,...
	'Sliderstep',[.05,.01],...
	'Callback',@slider_update,...
	'Style','slider');


% Text for beta
AMB_Data.uicontrols(3)=uicontrol('Units','normalized', ...
	'BackgroundColor',get(gcf,'Color'), ...
	'HorizontalAlignment','left', ...
	'Position',[.5,.78,.3,.05],...
	'String','beta=0.2500', ...
	'Style','text');

% Slider for beta
AMB_Data.uicontrols(4)=uicontrol('Units','normalized', ...
	'BackgroundColor',get(gcf,'Color'), ...
	'Position',[.05,.78,.4,.05], ...
	'Min',-1,'Max',1,'Value',.25,...
	'Sliderstep',[.05,.01],...
	'Callback',@slider_update,...
	'Style','slider');


% Button for next
AMB_Data.uicontrols(5)=uicontrol('Units','normalized', ...
	'BackgroundColor',get(gcf,'Color'), ...
	'String','Refine', ...
	'Enable','On', ...
	'Position',[.85,.85,.10,.05], ...
	'Callback',@next,...
	'Style','pushbutton');

% Button for restart
AMB_Data.uicontrols(6)=uicontrol('Units','normalized', ...
	'BackgroundColor',get(gcf,'Color'), ...
	'String','Restart', ...
	'Position',[.85,.78,.10,.05], ...
	'Callback',@restart,...
	'Style','pushbutton');

% Axis 
AMB_Data.axis(1)=subplot('position',[.05,.07,.9,.7]);
view(3);rotate3d on;
restart;

%%% Callback Functions %%%
function restart(varargin) 
global AMB_Data;
v = [0,sqrt(3),0;.5,-sqrt(3)/6,0;-.5,-sqrt(3)/6,0];
z = [0,0,.25];
z = [z;z;z];
data.v = [v;2/3*v;2/3*v+z;1/3*v+z];
data.e = [1,2;1,3;1,4;1,7;2,3;2,5;2,8;3,6;3,9;4,5;4,6;5,6;7,8;7,9;...
    8,9;10,11;10,12;11,12;10,4;11,5;12,6;7,10;8,11;9,12];
data.fv = [1,2,5,4;2,3,6,5;3,1,4,6;1,2,8,7;2,3,9,8;3,1,7,9;7,8,11,10;...
    8,9,12,11;9,7,10,12;10,11,5,4;11,12,6,5;12,10,6,4];
data.fe = [1,6,10,3;5,8,12,6;2,3,11,8;1,7,13,4;5,9,15,7;2,4,14,9;13,23,16,22;15,24,18,23;...
    14,22,17,24;16,20,10,19;18,21,12,20;...
    17,19,11,21]
% AMB_Data.v=[0 0 0;1 0 0;0 1 0;1 1 0;0 0 1;1 0 1;0 1 1;1 1 1];
% AMB_Data.e=[1 2;3 4;5 6;7 8;1 3;2 4;5 7;6 8;1 5;2 6;3 7;4 8];
% AMB_Data.fv=[1 2 4 3;5 6 8 7;1 2 6 5;3 4 8 7;1 3 7 5;2 4 8 6];
% AMB_Data.fe=[1 2 5 6;3 4 7 8;1 3 9 10;2 4 11 12;5 7 9 11;6 8 10 12];
AMB_Data.alpha=1.5;                 
AMB_Data.beta=.25;                 
AMB_Data.step=0;
set(AMB_Data.uicontrols(1),'String',sprintf('alpha=%06.4f',AMB_Data.alpha));
set(AMB_Data.uicontrols(3),'String',sprintf('beta=%06.4f',AMB_Data.beta));
set(AMB_Data.uicontrols(2),'Value',AMB_Data.alpha);
set(AMB_Data.uicontrols(4),'Value',AMB_Data.beta);
set(AMB_Data.uicontrols(5),'String','Refine');  
catmull_clark_subdivision;
myplot;

function slider_update(varargin) 
global AMB_Data;
% Read t value
AMB_Data.alpha = get(AMB_Data.uicontrols(2),'Value');
AMB_Data.beta = get(AMB_Data.uicontrols(4),'Value');
AMB_Data.step=0;
set(AMB_Data.uicontrols(1),'String',sprintf('alpha=%06.4f',AMB_Data.alpha));
set(AMB_Data.uicontrols(3),'String',sprintf('beta=%06.4f',AMB_Data.beta));
set(AMB_Data.uicontrols(5),'String','Refine');  
catmull_clark_subdivision;
myplot;

function next(varargin) 
global AMB_Data;
if AMB_Data.step < 6
  AMB_Data.step =AMB_Data.step+1; 
  set(AMB_Data.uicontrols(5),'String','Next');  
end
if AMB_Data.step == 6
  set(AMB_Data.uicontrols(5),'String','Refine');  
  refine
end
myplot;

%%% Internal Functions %%%
function refine
global AMB_Data;
AMB_Data.v=AMB_Data.vn;
AMB_Data.e=AMB_Data.en;
AMB_Data.fv=AMB_Data.fvn;
AMB_Data.fe=AMB_Data.fen;
AMB_Data.step=0;
catmull_clark_subdivision;
myplot;

function myplot
global AMB_Data;
cla;
hold on
axis equal;
axis off

% plot surface
if AMB_Data.step == 0
  X=reshape(AMB_Data.v(AMB_Data.fv',1),size(AMB_Data.fv')); 
  Y=reshape(AMB_Data.v(AMB_Data.fv',2),size(AMB_Data.fv')); 
  Z=reshape(AMB_Data.v(AMB_Data.fv',3),size(AMB_Data.fv')); 
  patch(X,Y,Z,Z);
  colormap winter;
  axis image
  return;
end

% frame
if AMB_Data.step > 0
  plot3([AMB_Data.v(AMB_Data.e(:,1),1),AMB_Data.v(AMB_Data.e(:,2),1)]',...
	[AMB_Data.v(AMB_Data.e(:,1),2),AMB_Data.v(AMB_Data.e(:,2),2)]',...
	[AMB_Data.v(AMB_Data.e(:,1),3),AMB_Data.v(AMB_Data.e(:,2),3)]','-k');
end

% face points
if AMB_Data.step > 1
  if AMB_Data.step == 2
    plot3(AMB_Data.fp(:,1),AMB_Data.fp(:,2),AMB_Data.fp(:,3),'or','markerfacecolor','r');
  else     
    plot3(AMB_Data.fp(:,1),AMB_Data.fp(:,2),AMB_Data.fp(:,3),'or');
  end
end

% edge points
if AMB_Data.step > 2
  if AMB_Data.step == 3
    plot3(AMB_Data.ep(:,1),AMB_Data.ep(:,2),AMB_Data.ep(:,3),'og','markerfacecolor','g');
  else     
    plot3(AMB_Data.ep(:,1),AMB_Data.ep(:,2),AMB_Data.ep(:,3),'og');
  end
end

% vertex points
if AMB_Data.step > 3
  if AMB_Data.step == 4
    plot3(AMB_Data.vp(:,1),AMB_Data.vp(:,2),AMB_Data.vp(:,3),'ob', ...
	  'markerfacecolor','b');
  else
    plot3(AMB_Data.vp(:,1),AMB_Data.vp(:,2),AMB_Data.vp(:,3),'ob');
  end
end

% new frame
if AMB_Data.step > 4
  plot3([AMB_Data.vn(AMB_Data.en(:,1),1),AMB_Data.vn(AMB_Data.en(:,2),1)]',...
	[AMB_Data.vn(AMB_Data.en(:,1),2),AMB_Data.vn(AMB_Data.en(:,2),2)]',...
	[AMB_Data.vn(AMB_Data.en(:,1),3),AMB_Data.vn(AMB_Data.en(:,2),3)]','-k');
end
axis image

function catmull_clark_subdivision
global AMB_Data;

v=AMB_Data.v;
e=AMB_Data.e;
fv=AMB_Data.fv;
fe=AMB_Data.fe;

nf=size(fv,1);
ne=size(e,1);
nv=size(v,1);

%%%%% FIND fp %%%%%
for k=1:nf
  fp(k,1:3)=mean(v(fv(k,:),:)); 
  %^ fp = face points
  %^ find new face points (mean of vertices that define the face)
end  

%%%%% FIND ep %%%%%%
for k=1:ne
  indf=find(sum(fe==k,2));
  %^ indf = index for faces that share edge k 
  %^ 2 faces per edge for closed shape
  ep(k,1:3)=mean([v(e(k,:),:);fp(indf,:)]); 
  %^ ep = edge point
  %^ take average of vertices that define the edge, and the average of the
  %^ faces that share that edge in common, then average those two things
  emp(k,1:3)=mean([v(e(k,:),:)]);
  %^ emp = edge midpoint
  %^ takes the average of the vertices that defines an edge
end    

%%%%% FIND vp %%%%%%
for k=1:nv
  indf=find(sum(fv==k,2)); 
  %^ indf = index for faces that share vertex k
  %^ at least 3 faces per vertex for closed shape
  inde=find(sum(e==k,2));
  %^ inde = index for edges that share vertex k
  %^ at least 3 edges per vertex for closed shape
  mn=length(indf);
  %^ mn = number of faces that share vertex k
  vp(k,:)=(1-2*AMB_Data.alpha/mn)*v(k,:)...
	 +2*(AMB_Data.alpha-2*AMB_Data.beta)/mn*mean(emp(inde,:))...
	 +4*AMB_Data.beta/mn*mean(fp(indf,:));
  % NOTE: Default alpha = 1.5, beta = .25
  %^ vp = new vertex point: moves original vertex based to barycenter
  %^      (center of mass) of fp,emp, and orginal point; alpha and beta
  %^      control weights of fp, emp, and the original point--default
  %^      values of alpha and beta give b-spline interpolation
  %^***** Let mn = n *****
  %^ line 1: (1-2(alpha)/n) = (1-2(1.5)/n) = (1-3/n)
  %^         = (n-3)/n --> coefficient for Catmull-Clark B-Spline surfaces
  %^ line 2: 2(alpha-2(beta))/n = 2(1.5 - 2(.5))/n = 2(1.5-.5)/n
  %^         = 2/n --> coefficient for Catmull-Clark B-Spline surfaces
  %^ line 3: 4(beta)/n = 4(.25)/n
  %^         = 1/n --> coefficient for Catmull-Clark B-Spline surfaces
end

%%%%% FIND vn = NEW VERTICES %%%%%
vn=[vp;ep;fp];
%^ each new point from vp, ep, and fp are new vertex points

AMB_Data.vp=vp;
AMB_Data.ep=ep;
AMB_Data.fp=fp;


% NOTE: Edges are defined between vp---ep and fp---ep

%%%%% DEFINE en = NEW EDGES %%%%%
% connects vp and ep
for k=1:ne
  en(k,1:2)=[e(k,1),nv+k];
  %^ e(k,1) takes column 1 indeces from e 
  %^ --> corresponds to vp points in vn
  %^ nv + k creates indeces starting after the number of vp points
  %^ --> corresponds to ep points in vn
  en(ne+k,1:2)=[nv+k,e(k,2)];
  %^ similar to above
end

for k=1:nf
  % k represents face label
  for k2=1:4
    % connects fp and ep
    en(2*ne+4*(k-1)+k2,1:2)=[nv+ne+k,nv+fe(k,k2)];
    %^ 2*ne+4*(k-1)+k2 --> corresponds to ep points in vn (does this in
    %^ chunks of 4 at a time (kth chunk of 4), where k2 cycles through each
    %^ of the four edges that defines the face)
    %
    %^ nv+ne+k --> corresponds to fp points in vn
    %^ nv+fe(k,k2) --> corresponds to ep point in vn where fe(k,:) gives
    %^ groups of four edges that define a face, and fe(k,k2) gives the 
    %^ index of ep in vn for one of those four edges
  end
  
  for k2=1:4
    rinde=find(sum(e(fe(k,:),:)==fv(k,k2),2))';
    %^ rinde = refined index edge
    %^ determines which edge uses the vp point defined by fv(k,k2)
    %^ give edge labels that share the vp point defined by fv(k,k2)
    fvn(4*(k-1)+k2,1:4)=[fv(k,k2),nv+fe(k,rinde(1)),nv+ne+k,nv+fe(k,rinde(2))];
    %^ fvn = face defined by new vertex point vn
    %^ fvn = index for each point in vn that we use to define a new face
    %^ fvn(1) = one point of vp in vn
    %^ fvn(2) = one point of ep in vn
    %^ fvn(3) = one point of fp in vn
    %^ fvn(4) = one point of ep in vn
    %^ fvn = [vp,ep,fp,ep]
    teind=[fe(k,rinde),fe(k,rinde)+ne];
    %^ index for rows in en that contain ep associated with the 4 edges
    %^ from rinde
    inde2=find(sum(en(teind,:)==fv(k,k2),2));
    %^ finds which of four rows of en (defined by teind) that contains 
    fen(4*(k-1)+k2,1:4)=[2*ne+4*(k-1)+rinde,teind(inde2)];
    %^ fen = face define by new edges en
    %^ 2*ne+4*(k-1)+rinde --> chooses the edge index from rows in en that
    %^ contain edges connecting fp and the two ep of the face
    %^ teind(inde2) --> gives edge index from rows in en that contain edges
    %^ connecting vp and the two ep of the face
  end  
end

AMB_Data.vn=vn;
AMB_Data.en=en;
AMB_Data.fvn=fvn;
AMB_Data.fen=fen;

