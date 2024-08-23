create database gt;

use gt;

create table Tarea(
	titulo varchar(30) primary key,
    descripcion text,
    f_vencimiento date not null,
    estado varchar(10) not null
);

create table TareaSimple(
	tarea varchar(30) primary key,
    importancia varchar(10) not null,
    foreign key(tarea) references tarea(titulo)
);

create table TareaRecurrente(
	tarea varchar(30) primary key,
    recurrencia int not null,
    foreign key(tarea) references tarea(titulo)
);