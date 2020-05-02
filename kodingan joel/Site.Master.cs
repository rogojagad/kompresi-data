using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

namespace Adaptive_Huffman
{
    public partial class SiteMaster : MasterPage
    {
        HuffmanTree huffmanTree = new HuffmanTree();
        protected void Page_Load(object sender, EventArgs e)
        {

        }

        protected void ButtonCompress_Click(object sender, EventArgs e)
        {
            string DataToCompress = File.ReadAllText(@"/Input.txt");
            
            huffmanTree.Build(DataToCompress);

            BitArray encoded = huffmanTree.Encode(DataToCompress);

            StreamWriter file = new StreamWriter(@"/Compressed_Input.txt");
            foreach (bool bit in encoded)
            {
                file.Write((bit ? 1 : 0));
            }
            file.Close();

            string decoded = huffmanTree.Decode(encoded);

            StreamWriter fileuncompressed = new StreamWriter(@"/Uncompressed_Input.txt");
            fileuncompressed.Write(decoded);
            fileuncompressed.Close();

        }

        protected void ButtonUncompress_Click(object sender, EventArgs e)
        {
            string DataToUncompress = File.ReadAllText(@"/Compressed_Input.txt");

            BitArray bitarray = new BitArray(DataToUncompress.Select(c => c == '1').ToArray());

            string decoded = huffmanTree.Decode(bitarray);

            StreamWriter file = new StreamWriter(@"/Uncompressed_Input.txt");
            file.Write(decoded);
            file.Close();
        }
    }
}