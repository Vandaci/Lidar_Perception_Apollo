points=[-2,3;-3,4;4,-5;2,1]
o=[0,0];
b=[8,1];
ns=nan(4,2);
height=nan(4,1);
figure();
plot(points(:,1),points(:,2),'Marker','o','MarkerFaceColor','g','LineStyle','none');
hold on 
plot([o(1),b(1)],[o(2),b(2)])
set(gca,'YLim',[-6,8],'XLim',[-2,10]);
axis equal
for i=1:4
    [ns(i,:),height(i)]=projpoint(o,b,points(i,:));
    text(points(i,1)+0.1,points(i,2)+0.1,num2str(i))
    plot([points(i,1),ns(i,1)],[points(i,2),ns(i,2)],'b')
end