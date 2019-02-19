% min_box sim 
clc,clear,close all
% step 1 : Randomly sprinkle points in the designated area and visualize
x=unifrnd(-30,-20,40,1);
y=unifrnd(-40,-20,40,1);
s_size=get(0,'ScreenSize');
fig=figure('Position',[s_size(3)/6,s_size(4)/6,s_size(3)*2/3,s_size(4)*2/3]);
fia=axes();
title(fia,'Sim Min Box')
plot(x,y,'Marker','o','MarkerFaceColor','Black','MarkerSize',2,'LineStyle','none')
axis equal
hold on 
plot(0,0,'pr','MarkerSize',10,'MarkerFaceColor','r')
text(2,0,'Lidar Center')
set(gca,'XLim',[-50,10],'YLim',[-50,10])
xlabel('X - m')
ylabel('Y - m')
box off
% step 2 : caculate boundary and visualize
dt=delaunayTriangulation(x,y);
bon=convexHull(dt);
plot(dt.Points(bon,1),dt.Points(bon,2))
% step 3 : Calculate the  gravity of the Points Cloud
bon_points=dt.Points(bon(1:end-1),:);
center_x=mean(bon_points(:,1));
center_y=mean(bon_points(:,2));
plot(center_x,center_y,'Color','green','Marker','^','MarkerSize',5,'MarkerFaceColor','green','LineStyle','none')
text(center_x+1,center_y,'Gravity')
% step 4 : sort use atan2
deg=atan2(bon_points(:,2)-center_y,bon_points(:,1)-center_x);
[~,idx]=sortrows(deg,'descend');
bon_points=bon_points(idx,:);
for i=1:length(bon_points)
    text(bon_points(i,1)+1,bon_points(i,2)+1,num2str(i),'FontSize',11)
end
% step 5 : find the max point and min point
min_points=bon_points(1,:);
max_points=bon_points(1,:);
min_idx=1;
max_idx=1;
for i=2:length(bon_points)
    tmp=bon_points(i,:);
    if max_points(1)*tmp(2)-tmp(1)*max_points(2)<0
        max_points(1)=tmp(1);
        max_points(2)=tmp(2);
        max_idx=i;
    end
    if min_points(1)*tmp(2)-tmp(1)*min_points(2)>0
        min_points(1)=tmp(1);
        min_points(2)=tmp(2);
        min_idx=i;
    end
end
plot([min_points(1),max_points(1)],[min_points(2),max_points(2)],'Marker','v','Color','b','LineStyle','none');
text(min_points(1)+3,min_points(2)-2,'Min Point')
text(max_points(1)-5,max_points(2)+3,'Max Point')
% step 6 : select valid line 
b_line=max_points-min_points;
v_b_idx=[];
for i=1:size(bon_points,1)
    idx=mod(min_idx+i,size(bon_points,1));
    if idx==0
        idx=size(bon_points,1);
    end
    tmp=bon_points(idx,:)-min_points;
    if b_line(1)*tmp(2)-tmp(1)*b_line(2)<0
        v_b_idx=[v_b_idx;idx];
    end
end   
v_b_idx=[max_idx;v_b_idx;min_idx];
plot(bon_points(v_b_idx,1),bon_points(v_b_idx,2),'LineStyle','--','Color','black','LineWidth',1);
rec=cell(length(v_b_idx)-1,1);
min_area=inf;
rec_idx=0;
for i=1:length(v_b_idx)-1
    rec{i}=rec4points(bon_points,[v_b_idx(i),v_b_idx(i+1)]);
    if rec{i}.area<min_area
        min_area=rec{i}.area;
        rec_idx=i;
    end
end
plot(rec{rec_idx}.rec4points(:,1),rec{rec_idx}.rec4points(:,2),'LineWidth',1.5)
legend('Points 2D','Lidar Center','Hull','Gravity','Max Min POint','Valid Boundary','Min Box','Location','northwest')
hold off
