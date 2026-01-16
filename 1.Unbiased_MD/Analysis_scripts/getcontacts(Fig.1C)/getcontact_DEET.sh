/data/software/getcontacts/get_dynamic_contacts.py --topology step6.6_equilibration.gro --trajectory nopbc.xtc --itypes all --output MD_all.tsv --sele2 'resname DE3'

for ((i=4;i<8;i++))
do
		echo "# total_frames:1001 beg:0 end:1000 stride:1 interaction_types:hp,sb,pc,ps,ts,vdw,hb
 Columns: frame, interaction_type, atom_1, atom_2[, atom_3[, atom_4]]" > MD_47${i}_all.tsv
               grep DE3:47${i} MD$_all.tsv >> MD_47${i}_all.tsv
               sed -i 's/X:DE3:474/X:LIG:999/g' MD_47${i}_all.tsv
               sed -i 's/X:DE3:475/X:LIG:999/g' MD_47${i}_all.tsv
              sed -i 's/X:DE3:476/X:LIG:999/g' MD_47${i}_all.tsv
               sed -i 's/X:DE3:477/X:LIG:999/g' MD_47${i}_all.tsv
done

python /data/software/getcontacts/get_contact_frequencies.py --input_files MD_474_all.tsv MD_475_all.tsv MD_476_all.tsv MD_477_all.tsv  --output_file MD_hb.tsv --itypes hb
python /data/software/getcontacts/get_contact_frequencies.py --input_files MD_474_all.tsv MD_475_all.tsv MD_476_all.tsv MD_477_all.tsv  --output_file MD_wb2.tsv --itypes wb2
python /data/software/getcontacts/get_contact_frequencies.py --input_files MD_474_all.tsv MD_475_all.tsv MD_476_all.tsv MD_477_all.tsv  --output_file MD_lwb.tsv --itypes lwb
python /data/software/getcontacts/get_contact_frequencies.py --input_files MD_474_all.tsv MD_475_all.tsv MD_476_all.tsv MD_477_all.tsv  --output_file MD_lwb2.tsv --itypes lwb2
