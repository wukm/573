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
AMB_Data.v=[0 0 0;1 0 0;0 1 0;1 1 0;0 0 1;1 0 1;0 1 1;1 1 1];
AMB_Data.e=[1 2;3 4;5 6;7 8;1 3;2 4;5 7;6 8;1 5;2 6;3 7;4 8];
AMB_Data.fv=[1 2 4 3;5 6 8 7;1 2 6 5;3 4 8 7;1 3 7 5;2 4 8 6];
AMB_Data.fe=[1 2 5 6;3 4 7 8;1 3 9 10;2 4 11 12;5 7 9 11;6 8 10 12];
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

for k=1:nf
  fp(k,1:3)=mean(v(fv(k,:),:));
end  

for k=1:ne
  indf=find(sum(fe==k,2));
  ep(k,1:3)=mean([v(e(k,:),:);fp(indf,:)]);
  emp(k,1:3)=mean([v(e(k,:),:)]);
end    

for k=1:nv
  indf=find(sum(fv==k,2));
  inde=find(sum(e==k,2));
  mn=length(indf);
  vp(k,:)=(1-2*AMB_Data.alpha/mn)*v(k,:)...
	 +2*(AMB_Data.alpha-2*AMB_Data.beta)/mn*mean(emp(inde,:))...
	 +4*AMB_Data.beta/mn*mean(fp(indf,:));
end

vn=[vp;ep;fp];

AMB_Data.vp=vp;
AMB_Data.ep=ep;
AMB_Data.fp=fp;

for k=1:ne
  en(k,1:2)=[e(k,1),nv+k];
  en(ne+k,1:2)=[nv+k,e(k,2)];
end

for k=1:nf
  for k2=1:4
    en(2*ne+4*(k-1)+k2,1:2)=[nv+ne+k,nv+fe(k,k2)];
  end
  
  for k2=1:4
    rinde=find(sum(e(fe(k,:),:)==fv(k,k2),2))';
    fvn(4*(k-1)+k2,1:4)=[fv(k,k2),nv+fe(k,rinde(1)),nv+ne+k,nv+fe(k,rinde(2))];
    teind=[fe(k,rinde),fe(k,rinde)+ne];
    inde2=find(sum(en(teind,:)==fv(k,k2),2));
    fen(4*(k-1)+k2,1:4)=[2*ne+4*(k-1)+rinde,teind(inde2)];
  end  
end

AMB_Data.vn=vn;
AMB_Data.en=en;
AMB_Data.fvn=fvn;
AMB_Data.fen=fen;


