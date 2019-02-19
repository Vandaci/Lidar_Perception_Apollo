% bon_points 边界点的坐标，已经排好序的
% line_idx 索引边 1 by 2
function out=rec4point(bon_points,line_idx)
    out=struct();
    out.ns=nan(size(bon_points,1),2);
    out.height=nan(size(bon_points,1),1);
    out.k=bon_points(line_idx,:);
    out.k=out.k(1,:)-out.k(2,:);
    out.k=out.k(2)/out.k(1);
    for i=1:size(bon_points,1)
        [out.ns(i,:),out.height(i)]=projpoint(bon_points(line_idx(1),:),bon_points(line_idx(2),:),bon_points(i,:));
    end
    if out.k>0
        out.min_bon_idx=find(out.ns(:,1)==min(out.ns(:,1))&out.ns(:,2)==min(out.ns(:,2)));
        out.max_bon_idx=find(out.ns(:,1)==max(out.ns(:,1))&out.ns(:,2)==max(out.ns(:,2)));
    elseif out.k<0
        out.min_bon_idx=find(out.ns(:,1)==min(out.ns(:,1))&out.ns(:,2)==max(out.ns(:,2)));
        out.max_bon_idx=find(out.ns(:,1)==max(out.ns(:,1))&out.ns(:,2)==min(out.ns(:,2)));        
    elseif out.k==0
        out.min_bon_idx=find(out.ns(:,1)==min(out.ns(:,1)));
        out.max_bon_idx=find(out.ns(:,1)==max(out.ns(:,1)));
    else
        out.min_bon_idx=find(out.ns(:,2)==min(out.ns(:,2)));
        out.max_bon_idx=find(out.ns(:,2)==max(out.ns(:,2)));    
    end
    [out.max_height,max_height_idx]=max(out.height);
    len=bon_points(out.min_bon_idx,:)-bon_points(out.max_bon_idx,:);
    out.len=sqrt(len(1)^2+len(2)^2);
    if out.max_height>out.len
        out.wid=out.len;
        out.len=out.max_height;
    else
        out.wid=out.max_height;
    end
    out.area=out.len*out.max_height;
    % 求四顶点画图
    out.rec4points=nan(5,2);
    out.rec4points(1:2,:)=out.ns([out.min_bon_idx,out.max_bon_idx],:);
    ns1=out.rec4points(1,:);
    ns0=out.rec4points(2,:);
    out.rec4points(3,:)=projpoint(ns0,[ns0(2)*(ns1(2)-ns0(2))/(ns1(1)-ns0(1))+ns0(1),1],bon_points(max_height_idx,:));
    out.rec4points(4,:)=projpoint(ns1,[ns1(2)*(ns0(2)-ns1(2))/(ns0(1)-ns1(1))+ns1(1),1],bon_points(max_height_idx,:));
    out.rec4points(5,:)=out.rec4points(1,:);
    out.direction=ns0-ns1;
end