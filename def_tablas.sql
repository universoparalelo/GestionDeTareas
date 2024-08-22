create database gt;

use gt;

create table Tarea(
	titulo varchar(30) primary key,
    descripcion text,
    f_vencimiento date not null,
    estado varchar(10) not null
);

create table TareaSimple(
	titulo varchar(30) primary key,
    importancia varchar(10) not null,
    foreign key(titulo) references tarea(titulo)
);

create table TareaRecurrente(
	titulo varchar(30) primary key,
    recurrencia int not null,
    foreign key(titulo) references tarea(titulo)
);