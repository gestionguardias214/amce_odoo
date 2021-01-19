CREATE OR REPLACE FUNCTION precio_guardia(integer) RETURNS double precision
                as '
                select 
                pca_precio
                from asw_guardia gua
                join asw_precio_categoria as pc on pca_categoria = gua_categoria AND pca_fecha <= gua_ingreso
                where gua.id = $1
                order by pc.id desc
                limit 1'
                LANGUAGE SQL
                IMMUTABLE
                RETURNS NULL on NULL INPUT;

update asw_guardia set gua_precioxhora = precio_guardia(id) where gua_precioxhora is null;