// Generated with Prismap, written by Jim DeVona
// https://github.com/anoved/prismap

inflation = 1000;
minlat = 40.4416 * inflation;
maxlat = 40.4461 * inflation;
minlon = -79.94850 * inflation;
maxlon = -79.9471442 * inflation;

n1 = [40.4459042, -79.9484471] * inflation;
n2 = [40.4460545, -79.9484642] * inflation;
n3 = [40.4460675, -79.9482668] * inflation;
n4 = [40.4459173, -79.9482496] * inflation;

s1 = [40.4420146, -79.9474045] * inflation;
s2 = [40.4416749, -79.9475333] * inflation;
s3 = [40.4416227, -79.9472844] * inflation;
s4 = [40.4416961, -79.9472643] * inflation;
s5 = [40.4416880, -79.9472157] * inflation;
s6 = [40.4416423, -79.9472071] * inflation;
s7 = [40.4416357, -79.9470784] * inflation;
s8 = [40.4416814, -79.9470269] * inflation;
s9 = [40.4417402, -79.9470355] * inflation;
s10 = [40.4417941, -79.9471442] * inflation;
s11 = [40.4417745, -79.9471785] * inflation;
s12 = [40.4417860, -79.9472243] * inflation;
s13 = [40.4419623, -79.9471642] * inflation;

building1 = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13];

x_size_limit = 200;
y_size_limit = 200;

x_scale = x_size_limit / (maxlat - minlat);
y_scale = y_size_limit / (maxlon - minlon);

x_trans = -(minlat+maxlat) / 2;
y_trans = -(minlon+maxlon) / 2;

VegeGarden();

module feature0() {
		//translate([bx, by, 0]) scale([1, 1, 1]) 
		linear_extrude(height=200) polygon(points=[
			n1, n2, n3, n4]);
}

module feature1() {
		//translate([bx, by, 0]) scale([1, 1, 1]) 
		linear_extrude(height=200) polygon(points=building1);
}

module printStat(){
	echo("x_scale: ", x_scale, " y_scale: ", y_scale);
	echo("x_trans: ", x_trans, " y_trans: ", y_trans);
}

module VegeGarden() {
	translate([-50, -50, -50]){
		cube([100, 100, 100]);
	}
	printStat();
	scale([x_scale, y_scale, 1]) 
	translate([x_trans, y_trans, 0]){
		feature0();
		feature1();
	}
}
