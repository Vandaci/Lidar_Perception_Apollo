% 求oa在ob上的投影点坐标
function [pos,height]=projpoint(o,b,a)
    oa=a-o;
    ob=b-o;
    op=(oa(1)*ob(1)+oa(2)*ob(2))*(ob)/(ob(1)^2+ob(2)^2);
    pos=op+o;
    height=abs((oa(1)*ob(2)-oa(2)*ob(1))/sqrt(ob(1)^2+ob(2)^2));
end