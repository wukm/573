function catmull_clark
    % noninteractive version
    
    % which iterations you want a figure of
    end_step = 2;
    
    % default is cube; change to whatever
    global data;
    data=[];
    data.v=[0 0 0;1 0 0;0 1 0;1 1 0;0 0 1;1 0 1;0 1 1;1 1 1];
    data.e=[1 2;3 4;5 6;7 8;1 3;2 4;5 7;6 8;1 5;2 6;3 7;4 8];
    data.fv=[1 2 4 3;5 6 8 7;1 2 6 5;3 4 8 7;1 3 7 5;2 4 8 6];
    data.fe=[1 2 5 6;3 4 7 8;1 3 9 10;2 4 11 12;5 7 9 11;6 8 10 12];
    data.alpha=1.5;                 
    data.beta=.25;  
    data.step = 0;

for step=1:end_step
    catmull_clark_subdivision;
    data.v = data.vn;
    data.e = data.en;
    data.fv = data.fvn;
    data.fe = data.fen;
    data.step = data.step + 1;
end;

data.axis(1)=subplot('position',[.05,.07,.9,.7]);
view(3);rotate3d on;
myplot;

function myplot
global data;
cla;
hold on
axis equal;
axis off

% plot surface

X=reshape(data.v(data.fv',1),size(data.fv')); 
Y=reshape(data.v(data.fv',2),size(data.fv')); 
Z=reshape(data.v(data.fv',3),size(data.fv')); 
patch(X,Y,Z,Z);
colormap winter;
axis image

title(['Catmull Clark Subdivision (step=', num2str(data.step), ')']);
% frame
plot3([data.v(data.e(:,1),1),data.v(data.e(:,2),1)]',...
	[data.v(data.e(:,1),2),data.v(data.e(:,2),2)]',...
	[data.v(data.e(:,1),3),data.v(data.e(:,2),3)]','-k');

% face points
face_points = plot3(data.fp(:,1),data.fp(:,2),data.fp(:,3),...
    'or','markerfacecolor','r','DisplayName', 'face points');
%plot3(data.fp(:,1),data.fp(:,2),data.fp(:,3),'or');

% edge points
edge_points = plot3(data.ep(:,1),data.ep(:,2),data.ep(:,3),'og','markerfacecolor','g',...
    'DisplayName', 'edge points');
%plot3(data.ep(:,1),data.ep(:,2),data.ep(:,3),'og');

% vertex points
vertex_points = plot3(data.vp(:,1),data.vp(:,2),data.vp(:,3),'ob', ...
	  'markerfacecolor','b', 'DisplayName', 'vertex points');
%plot3(data.vp(:,1),data.vp(:,2),data.vp(:,3),'ob');

plot3([data.vn(data.en(:,1),1),data.vn(data.en(:,2),1)]',...
	[data.vn(data.en(:,1),2),data.vn(data.en(:,2),2)]',...
	[data.vn(data.en(:,1),3),data.vn(data.en(:,2),3)]','-k');

legend([face_points,edge_points, vertex_points]);
axis image
return;

function catmull_clark_subdivision
global data;



v=data.v;
e=data.e;
fv=data.fv;
fe=data.fe;

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
  vp(k,:)=(1-2*data.alpha/mn)*v(k,:)...
	 +2*(data.alpha-2*data.beta)/mn*mean(emp(inde,:))...
	 +4*data.beta/mn*mean(fp(indf,:));
end

vn=[vp;ep;fp];

data.vp=vp;
data.ep=ep;
data.fp=fp;

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

data.vn=vn;
data.en=en;
data.fvn=fvn;
data.fen=fen;


